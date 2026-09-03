(function () {
  'use strict';

  var target = document.getElementById('course-content');
  if (!target) return;

  function esc(value) {
    return String(value == null ? '' : value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function trusted(value) {
    return String(value == null ? '' : value);
  }

  function renderTopics(course) {
    return '<h2>Main Topics</h2><div class="topic-pills">' + (course.topics || []).map(function (topic) {
      return '<span class="topic-pill">' + esc(topic.icon) + ' ' + esc(topic.name) + '</span>';
    }).join('') + '</div>';
  }

  function renderOrganization(course) {
    return '<h2>Organization</h2><div class="info-box"><div class="info-grid">' + (course.organization_summary || []).map(function (item) {
      return '<div class="info-item"><span class="icon">' + esc(item.icon) + '</span><div><strong>' + esc(item.label) + ':</strong> ' + esc(item.value) + '</div></div>';
    }).join('') + '</div></div>';
  }

  function renderLecture(lecture) {
    var title = esc(lecture.title);
    if (lecture.pdf) title = '<a href="' + esc(lecture.pdf) + '">' + title + '</a>';

    var html = '<div class="lecture-card"><h3><span class="lecture-badge">' + esc(lecture.id) + '</span>' + title + '</h3>';
    if (lecture.topics && lecture.topics.length) {
      html += '<ul>' + lecture.topics.map(function (topic) { return '<li>' + esc(topic) + '</li>'; }).join('') + '</ul>';
    }
    if (lecture.subdecks && lecture.subdecks.length) {
      html += '<ul>' + lecture.subdecks.map(function (deck) {
        return '<li><strong><a href="' + esc(deck.pdf) + '">' + esc(deck.title) + '</a></strong>' +
          (deck.description ? '<span class="subdeck-description">' + esc(deck.description) + '</span>' : '') + '</li>';
      }).join('') + '</ul>';
    }
    return html + '</div>';
  }

  function renderTd(td) {
    var html = '<div class="lecture-card td-card"><h3><span class="lecture-badge td">' + esc(td.id) + '</span>' + esc(td.title) + '</h3><ul>';
    if (td.handout) html += '<li><strong><a href="' + esc(td.handout) + '">📄 Handout (PDF)</a></strong>' + (td.description ? '<span class="subdeck-description">' + esc(td.description) + '</span>' : '') + '</li>';
    if (td.code && td.code.length) html += '<li><strong>💻 Python code:</strong> ' + td.code.map(function (file) { return '<a href="' + esc(file.url) + '">' + esc(file.label) + '</a>'; }).join(', ') + '</li>';
    if (td.code_repo) html += '<li><strong>💻 Code repository:</strong> <a href="' + esc(td.code_repo.url) + '" rel="noopener noreferrer">' + esc(td.code_repo.label) + '</a></li>';
    if (td.data && td.data.length) html += '<li><strong>📊 Data:</strong> ' + td.data.map(function (file) { return '<a href="' + esc(file.url) + '">' + esc(file.label) + '</a>'; }).join(', ') + '</li>';
    if (td.topics_summary) html += '<li><strong>📖 Topics:</strong> ' + esc(td.topics_summary) + '</li>';
    return html + '</ul></div>';
  }

  function renderSyllabus(syllabus) {
    return '<h2>General Syllabus</h2><p>The syllabus below combines the material covered across the different editions of the course.</p><div class="lecture-grid">' +
      (syllabus.lectures || []).map(renderLecture).join('') +
      (syllabus.tds || []).map(renderTd).join('') + '</div>';
  }

  function renderYears(course) {
    return '<h2 id="year-pages">Class Year Pages</h2><div class="year-grid">' + (course.years || []).map(function (year) {
      return '<div class="year-card"><a href="years/' + esc(year.year) + '.html">' + esc(year.label) + '</a></div>';
    }).join('') + '</div>';
  }

  function render(course, syllabus) {
    var html = '<div class="course-heading"><div><h2>Graphs in Machine Learning</h2>' +
      '<p class="course-kicker"><a href="' + esc(course.program_url) + '">' + esc(course.program) + '</a> · <a href="' + esc(course.institution_url) + '">' + esc(course.institution) + '</a></p></div>' +
      '<img src="/images/mva/peer_communities2.png" alt="Graph communities" loading="lazy" decoding="async"></div>';

    html += '<div class="intro-box"><strong>Teaching this course since 2014.</strong> Course materials from past years are available on the <a href="#year-pages">year pages</a> below. I have been teaching since 1996, including as a TA for <a href="/ta-cs0007-fall2005.html">CS7: Introduction to Programming</a> at the University of Pittsburgh in 2005.</div>';
    html += renderTopics(course);
    html += '<h2>Course Description</h2>' + (course.description || []).map(function (paragraph) { return '<p>' + esc(paragraph) + '</p>'; }).join('');
    html += renderOrganization(course);
    html += renderSyllabus(syllabus || {});
    html += '<h2>Recommended Reading</h2><ul class="reading-list">' +
      '<li>D. A. Spielman: <a href="https://cs-www.cs.yale.edu/homes/spielman/sagt/" rel="noopener noreferrer"><em>Spectral and Algebraic Graph Theory</em></a></li>' +
      '<li>G. L. Miller: <a href="https://www.cs.cmu.edu/afs/cs/academic/class/15859n-s20/index.html" rel="noopener noreferrer"><em>15-859N: Spectral Graph Theory</em></a></li>' +
      '<li>D. Easley and J. Kleinberg: <a href="https://www.cs.cornell.edu/home/kleinber/networks-book/" rel="noopener noreferrer"><em>Networks, Crowds, and Markets</em></a></li>' +
      '<li>U. von Luxburg: <a href="https://arxiv.org/abs/0711.0189" rel="noopener noreferrer"><em>A tutorial on spectral clustering</em></a></li>' +
      '<li>O. Chapelle, B. Schölkopf and A. Zien (eds.): <em>Semi-Supervised Learning</em></li>' +
      '<li>T. N. Kipf and M. Welling: <a href="https://arxiv.org/abs/1609.02907" rel="noopener noreferrer"><em>Semi-Supervised Classification with Graph Convolutional Networks</em></a></li>' +
      '<li>P. Veličković et al.: <a href="https://arxiv.org/abs/1710.10903" rel="noopener noreferrer"><em>Graph Attention Networks</em></a></li>' +
      '<li>M. Valko: <a href="/projects/bandits/index.html"><em>Bandits on Graphs and Structures</em></a></li></ul>';
    html += renderYears(course);
    target.innerHTML = html;
  }

  target.innerHTML = '<div class="info-box">Loading course materials…</div>';
  fetch('/mva-archive-data.json', { cache: 'no-cache' })
    .then(function (response) {
      if (!response.ok) throw new Error('HTTP ' + response.status);
      return response.json();
    })
    .then(function (data) { render(data.course || {}, data.syllabus || {}); })
    .catch(function (error) {
      console.error(error);
      target.innerHTML = '<div class="info-box"><strong>Course materials could not be loaded.</strong> Please refresh the page.</div>';
    });
})();
