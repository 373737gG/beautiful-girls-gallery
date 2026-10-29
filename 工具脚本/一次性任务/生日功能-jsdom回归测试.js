// 用 jsdom 加载 index.html，跑初始化 + 生日功能链路，捕获运行时错误
const fs = require('fs');
const { JSDOM } = require('jsdom');

const html = fs.readFileSync('D:/zhumian/工作区/项目归档/美少女图鉴/index.html', 'utf8');
const errors = [];
const dom = new JSDOM(html, {
  url: 'http://127.0.0.1:8899/index.html',
  runScripts: 'dangerously',
  pretendToBeVisual: true,
  beforeParse(window) {
    window.fetch = () => Promise.reject(new Error('no fetch in test'));
    window.matchMedia = window.matchMedia || (() => ({ matches: false, addListener(){}, removeListener(){} }));
    window.IntersectionObserver = class { constructor(cb){} observe(){} disconnect(){} unobserve(){} };
    window.HTMLMediaElement.prototype.play = function(){ return Promise.resolve(); };
    window.HTMLMediaElement.prototype.pause = function(){};
  },
});
dom.window.addEventListener('error', e => errors.push('window.onerror: ' + e.message));

const w = dom.window, d = w.document;
const A = (cond, msg) => { if (!cond) { console.log('FAIL:', msg); process.exit(1); } console.log('ok:', msg); };

setTimeout(() => {
  try {
    // 1. 初始化渲染
    A(d.querySelectorAll('.card').length > 0, `初始化渲染出卡片 (${d.querySelectorAll('.card').length} 张)`);
    A(d.getElementById('dash').textContent.includes('已知生日'), 'dash 含“已知生日”');
    A(d.getElementById('dash').textContent.includes('9'), '已知生日数=9');
    A(d.getElementById('bdayBanner').style.display === 'none', '10月无生日角色→横幅隐藏');

    // 2. 生日弹窗（默认当月10月 → 无角色）
    w.openBdayModal();
    A(d.getElementById('bdayModal').style.display === 'flex', '生日弹窗打开');
    A(d.getElementById('bdayTotal').textContent.includes('9'), '弹窗标题统计 9 人');
    A(d.querySelectorAll('.bday-month-btn').length === 12, '12个月份宫格');
    A(d.getElementById('bdayModalBody').textContent.includes('暂无'), '10月暂无角色提示');

    // 3. 切到8月 → 3个角色（真红/爱尔梅希尔德/初音未来）
    w.openBdayModal(8);
    const rows = d.querySelectorAll('.bday-row');
    A(rows.length === 3, `8月角色列表 3 人 (${rows.length})`);
    A(d.getElementById('bdayModalBody').textContent.includes('真红'), '列表含真红');
    A(d.getElementById('bdayModalBody').textContent.includes('初音未来'), '列表含初音未来');

    // 4. 点角色 → 关生日弹窗并打开详情
    rows[0].click();
    A(d.getElementById('bdayModal').style.display === 'none', '点角色后生日弹窗关闭');
    A(d.getElementById('viewModal').style.display === 'flex', '详情弹窗打开');
    w.closeModal('viewModal');

    // 5. 卡片生日行：搜索"8月"后 3 张卡片都应有生日行；首屏无生日角色则不应有该行
    const sb2 = d.getElementById('searchBox');
    sb2.value = '8月'; w.render();
    const augCards = d.querySelectorAll('.card');
    A(augCards.length === 3, `搜索8月 → 3 张卡片 (${augCards.length})`);
    A(d.querySelectorAll('.card-bday').length === 3, '3 张卡片全部带生日行');
    A([...d.querySelectorAll('.card-bday')].some(el => el.textContent.includes('8月13日')), '卡片显示“8月13日”');
    sb2.value = ''; w.render();
    A(d.querySelectorAll('.card-bday').length === 0, '首屏(id1-16)无生日角色→无生日行');

    // 6. 搜索生日关键词
    const sb = d.getElementById('searchBox');
    const search = q => { sb.value = q; w.render(); return d.querySelectorAll('.card').length; };
    A(search('8-13') === 1, `搜索 8-13 → 1 人 (${search('8-13')})`);
    A(search('0813') === 1, '搜索 0813 → 1 人');
    A(search('8月13日') === 1, '搜索 8月13日 → 1 人');
    const aug = search('8月');
    A(aug === 3, `搜索 8月 → 3 人 (${aug})`);
    // 6b. 普通词搜索不受生日逻辑影响（琳德：本人+desc提及的维尔姆，原有全文搜索行为）
    A(search('琳德') >= 1 && [...d.querySelectorAll('.card-name')].some(el => el.textContent === '琳德'), '普通词“琳德”仍可搜到');
    search('');

    // 7. 今天生日模拟：把今天日期改为 8-13 验证蛋糕与高亮
    const RealDate = w.Date;
    const bd = new RealDate(); // 今天 10-29；改为 8-13
    const fake = new RealDate(bd.getFullYear(), 7, 13);
    w.Date = class extends RealDate {
      constructor(...args) { if (args.length) super(...args); else super(fake.getTime()); }
      static now() { return fake.getTime(); }
    };
    search('8-13'); // 只显示真红（Shinku）1 张卡片
    A(d.getElementById('bdayBanner').style.display === 'flex', '模拟8月13日→横幅显示');
    A(d.getElementById('bdayBanner').textContent.includes('今天是真红（Shinku）的生日'), '横幅置顶加粗今天生日');
    A(d.querySelector('.card.today-card') !== null, '今天生日卡片金框类生效');
    A(d.querySelector('.card-bday').textContent.includes('今天生日'), '卡片生日行显示“今天生日！”');
    A(d.getElementById('bdayBanner').textContent.includes('共3人'), '横幅显示本月3人');
    w.Date = RealDate;
    w.render();
    A(d.getElementById('bdayBanner').style.display === 'none', '恢复真实日期→横幅隐藏');

    A(errors.length === 0, `无 JS 运行时错误 (${errors.length})`);
    if (errors.length) console.log(errors.join('\n'));
    console.log('ALL PASS');
    process.exit(0);
  } catch (e) {
    console.log('TEST ERROR:', e.message);
    if (errors.length) console.log(errors.join('\n'));
    process.exit(1);
  }
}, 1500);
