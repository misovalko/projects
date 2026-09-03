(function () {
    'use strict';

    var year = document.body.getAttribute('data-year');
    var target = document.getElementById('year-content');
    if (!year || !target) return;

    var dataBase = 'https://raw.githubusercontent.com/misovalko/misovalko.github.io/master/_data/mva';

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

    function absoluteOrRelative(url) {
        if (!url) return '';
        return /^(?:https?:)?\/\//i.test(url) ? url : url;
    }

    async function loadYaml(url) {
        var response = await fetch(url, { cache: 'no-cache' });
        if (!response.ok) throw new Error('HTTP ' + response.status + ' for ' + url);
        return jsyaml.load(await response.text());
    }

    function renderTopics(course, yd) {
        var topics = (course.topics || []).concat(yd.topics_extra || []);
        if (!topics.length) return '';
        return '<h2>Main topics</h2><div class="topic-pills">' + topics.map(function (topic) {
            return '<span class="topic-pill">' + esc(topic.icon) + ' ' + esc(topic.name) + '</span>';
        }).join('') + '</div>';
    }

    function renderNews(yd) {
        if (!yd.news || !yd.news.length) return '';
        return '<h2>News</h2><div class="news-box"><ul>' + yd.news.map(function (item) {
            return '<li><span class="note">' + esc(item.date) + ':</span> ' + trusted(item.text) + '</li>';
        }).join('') + '</ul></div>';
    }

    function renderAdmin(yd) {
        var admin = yd.admin || {};
        var rows = [];
        if (admin.time) rows.push('<li><strong>Time:</strong> ' + esc(admin.time) + '</li>');
        rows.push('<li><strong>Place:</strong> <a href="https://ens-paris-saclay.fr/">ENS Paris-Saclay</a> (different lecture halls)</li>');
        rows.push('<li><strong>7 or 8 lectures</strong> and <strong>3 recitations</strong> (TD/TP)</li>');
        rows.push('<li><strong>Validation:</strong> grades from practical sessions (40%) + class project (60%)</li>');
        rows.push('<li><strong>Research:</strong> projects, internships and PhD theses possible at SequeL and elsewhere</li>');
        if (admin.piazza) rows.push('<li><strong>Piazza:</strong> <a href="' + esc(admin.piazza) + '">registration and class discussion</a></li>');
        if (admin.ta) rows.push('<li><strong>TA:</strong> ' + esc(admin.ta) + '</li>');
        rows.push('<li><a href="https://www.master-mva.com/cours/graphs-in-machine-learning/">Course description</a> at MVA</li>');
        return '<h2>Administrivia</h2><div class="info-box"><ul style="margin:0;padding-left:1.2em">' + rows.join('') + '</ul></div>';
    }

    function renderWarnings(yd) {
        if (!yd.warnings || !yd.warnings.length) return '';
        return '<h2>Important: Don\'t take this class ...</h2><ul>' + yd.warnings.map(function (warning) {
            return '<li>' + esc(warning) + '</li>';
        }).join('') + '</ul>';
    }

    function renderIntro(course, yd) {
        if (yd.intro_override) return '<h2>Intro</h2><p>' + trusted(yd.intro_override) + '</p>';
        return '<h2>Intro</h2>' + (course.description || []).map(function (paragraph) {
            return '<p>' + esc(paragraph) + '</p>';
        }).join('');
    }

    function renderOrganization(course, yd) {
        var html = '<h2>Organization</h2><p>' + (yd.organization_override ? trusted(yd.organization_override) : trusted(course.organization || '')) + '</p>';
        if (!yd.hide_recitations) {
            html += '<h2>Recitations and homeworks (TDs)</h2><p>' + trusted(course.recitations || '') + '</p>';
        }
        return html;
    }

    function renderProjects(yd) {
        var p = yd.projects_info;
        if (!p) return '';
        var html = '<h2>Class projects</h2><p>The main part of the grade comes from the projects. Students are encouraged to choose a topic related to the course and start early. ';
        if (p.piazza_url) html += 'Some <a href="' + esc(p.piazza_url) + '">project proposals</a> are available. ';
        if (p.proposals_date) html += 'Additional proposals are presented on <strong>' + esc(p.proposals_date) + '</strong>. ';
        if (p.decision_deadline) html += 'The decision deadline is <strong>' + esc(p.decision_deadline) + '</strong>. ';
        if (p.recommended_date) html += 'The recommended date for choosing a project is ' + esc(p.recommended_date) + '. ';
        if (p.report_deadline) {
            html += 'The report deadline is <strong>' + esc(p.report_deadline) + '</strong>';
            if (p.format_url) html += ' in <a href="' + esc(p.format_url) + '">' + esc(p.format_label || 'the required') + ' format</a>';
            html += '. ';
        }
        if (p.presentation_text) html += trusted(p.presentation_text) + ' ';
        html += 'Students can work in pairs of 2 and exceptionally 3.';
        if (p.piazza_url) html += ' Detailed instructions are on the <a href="' + esc(p.piazza_url) + '">class projects page</a>.';
        return html + '</p>';
    }

    function renderPolicies(course, yd) {
        var html = '';
        if (!yd.hide_registration) html += '<h2>Registration, Communication, and Questions</h2><p>' + trusted(course.registration || '') + '</p>';
        if (!yd.hide_late_policy) html += '<h2>Late policy</h2><p>' + esc(course.late_policy || '') + '</p>';
        html += '<h2>Prerequisites</h2><p>' + esc(course.prerequisites || '') + '</p>';
        return html;
    }

    function renderSyllabus(yd) {
        if (!yd.syllabus || !yd.syllabus.length) return '';
        var cards = yd.syllabus.map(function (item) {
            if (item.type === 'break') {
                var papers = '';
                if (item.papers && item.papers.length) {
                    papers = '<p style="margin:.5em 0">Papers presented at ' + esc(item.reason) + ':</p><ul>' + item.papers.map(function (paper) {
                        var title = '<em>' + esc(paper.title) + '</em>';
                        return '<li>' + (paper.url ? '<a href="' + esc(paper.url) + '">' + title + '</a>' : title) + '</li>';
                    }).join('') + '</ul>';
                }
                return '<div class="lecture-card" style="background:#fefce8"><h3><span class="note">No class - ' + esc(item.date) + ' - ' + esc(item.reason) + '</span></h3>' + papers + '</div>';
            }

            var href = item.pdf || item.url || '';
            var title = esc(item.title || item.id || 'Session') + esc(item.title_suffix || '');
            if (href) title = '<a href="' + esc(absoluteOrRelative(href)) + '"' + (item.url ? ' rel="noopener noreferrer"' : '') + '>' + title + '</a>';
            var badgeClass = item.type === 'td' ? ' td' : '';
            var meta = item.date || item.room ? '<span class="note">' + esc(item.date || '') + (item.room ? ', ' + esc(item.room) : '') + '</span>' : '';
            var guest = item.guest ? '<p style="margin:.5em 0">Invited lecture by <a href="' + esc(item.guest.url) + '" rel="noopener noreferrer">' + esc(item.guest.name) + '</a></p>' : '';
            var topics = item.topics && item.topics.length ? '<ul>' + item.topics.map(function (topic) { return '<li>' + esc(topic) + '</li>'; }).join('') + '</ul>' : '';
            return '<div class="lecture-card"><h3><span class="lecture-badge' + badgeClass + '">' + esc(item.id) + '</span>' + title + ' ' + meta + '</h3>' + guest + topics + '</div>';
        }).join('');
        return '<h2>Syllabus</h2><div class="lecture-grid">' + cards + '</div>';
    }

    function renderDeadlines(yd) {
        if (!yd.deadlines || !yd.deadlines.length) return '';
        return '<div class="info-box"><p style="margin:0"><strong>📅 Important dates:</strong></p><ul style="margin:.5em 0 0;padding-left:1.2em">' + yd.deadlines.map(function (deadline) {
            return '<li><span class="note">' + esc(deadline.date) + ':</span> ' + esc(deadline.label) + '</li>';
        }).join('') + '</ul></div>';
    }

    function renderYearLinks(course, yd) {
        var cards = '<div class="year-card"><a href="../index.html">Main page</a></div>';
        cards += (course.years || []).filter(function (item) { return item.year !== yd.year; }).map(function (item) {
            return '<div class="year-card"><a href="' + esc(item.year) + '.html">' + esc(item.label) + '</a></div>';
        }).join('');
        return '<h2>Class Year Pages</h2><div class="year-grid">' + cards + '</div>';
    }

    function render(course, yd) {
        document.title = 'Michal Valko - ' + yd.title;
        var html = '';
        html += '<a href="https://www.master-mva.com/" style="background:none;padding-right:0"><img src="../../../images/mva/mva_bandeau.png" style="max-width:100%;height:auto;display:block;margin:0 auto" alt="MVA Bandeau" loading="lazy"></a>';
        html += '<img width="105" src="../../../images/mva/peer_communities2.png" style="float:right;margin:5px 0 10px 10px" alt="Peer Communities" loading="lazy">';
        html += '<h1>' + esc(yd.title) + '</h1><p><a href="https://www.master-mva.com/">MVA</a> - <a href="https://ens-paris-saclay.fr/">ENS Paris-Saclay</a></p>';
        html += renderNews(yd);
        html += renderAdmin(yd);
        html += renderTopics(course, yd);
        html += renderWarnings(yd);
        html += renderIntro(course, yd);
        html += renderOrganization(course, yd);
        html += renderProjects(yd);
        html += renderPolicies(course, yd);
        html += renderSyllabus(yd);
        html += renderDeadlines(yd);
        html += renderYearLinks(course, yd);
        target.innerHTML = html;
    }

    target.innerHTML = '<div class="info-box">Loading course archive...</div>';
    Promise.all([
        loadYaml(dataBase + '/course.yml'),
        loadYaml(dataBase + '/years/' + encodeURIComponent(year) + '.yml')
    ]).then(function (values) {
        render(values[0], values[1]);
    }).catch(function (error) {
        console.error(error);
        target.innerHTML = '<div class="info-box"><strong>Course archive data could not be loaded.</strong><br><a href="../index.html">Return to the MVA course page</a>.</div>';
    });
})();
