(() => {
  const escapeHtml = (value) => String(value ?? '').replace(/[&<>"']/g, (char) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
  }[char]));

  const style = document.createElement('style');
  style.textContent = `
    .workforce-mascot { display:inline-flex; position:relative; align-items:center; justify-content:center; width:24px; height:24px; margin-left:4px; margin-right:8px; color:inherit; background:transparent; font-size:13px; line-height:1; vertical-align:middle; }
    .workforce-mascot .mascot-face { display:block; transform-origin:center bottom; font-family:"Apple Color Emoji","Segoe UI Emoji","Noto Color Emoji",sans-serif; animation:mascot-breathe 2.8s ease-in-out infinite; }
    .workforce-mascot .mascot-z { position:absolute; top:-13px; right:-7px; color:#a8d84e; font:800 10px DM Mono,monospace; opacity:0; }
    .workforce-mascot .mascot-z.z-two { top:-20px; right:-1px; font-size:8px; }
    .workforce-mascot .mascot-z.z-three { top:-25px; right:7px; font-size:7px; }
    body.dark .workforce-mascot .mascot-face { animation:mascot-sleep 3.2s ease-in-out infinite; }
    body.dark .workforce-mascot .mascot-z { animation:mascot-snore 2.4s ease-out infinite; }
    body.dark .workforce-mascot .mascot-z.z-two { animation-delay:.55s; }
    body.dark .workforce-mascot .mascot-z.z-three { animation-delay:1.1s; }
    @keyframes mascot-breathe { 50% { transform:translateY(-2px) rotate(-4deg); } }
    @keyframes mascot-sleep { 50% { transform:translateY(2px) scaleY(.94) rotate(4deg); } }
    @keyframes mascot-snore { 0% { opacity:0; transform:translate(2px,5px) scale(.7); } 35%,70% { opacity:1; } 100% { opacity:0; transform:translate(10px,-10px) scale(1.15); } }
    @media (prefers-reduced-motion:reduce) { .workforce-mascot .mascot-face,.workforce-mascot .mascot-z { animation:none; } body.dark .workforce-mascot .mascot-z { opacity:1; } }
    .crm-form { display:grid; grid-template-columns:1.4fr 1fr 1.2fr auto; gap:10px; padding:18px; }
    .crm-form input,.crm-form select { min-width:0; padding:11px 12px; border:1px solid var(--line); border-radius:9px; color:var(--ink); background:var(--surface); outline:0; font-size:12px; }
    .crm-form input:focus,.crm-form select:focus { border-color:#8eb879; box-shadow:0 0 0 3px rgba(142,184,121,.18); }
    .crm-table { overflow:auto; }
    .crm-row { display:grid; grid-template-columns:1.5fr .8fr 1fr 1fr 1fr auto; min-width:780px; gap:14px; align-items:center; padding:14px 18px; border-bottom:1px solid var(--line); }
    .crm-row:last-child { border-bottom:0; }
    .crm-row.header { color:var(--muted); font:500 10px DM Mono,monospace; text-transform:uppercase; }
    .crm-company { font-size:12px; font-weight:800; }
    .crm-actions { display:flex; gap:6px; }
    .crm-action { padding:6px 8px; border-radius:6px; color:var(--deep); background:var(--soft); font-size:10px; font-weight:800; }
    .crm-action.delete { color:#9b4c3c; background:#fce5de; }
    @media (max-width:760px) { .crm-form { grid-template-columns:1fr; } }
  `;
  document.head.appendChild(style);

  const nav = document.querySelector('.nav[aria-label="Primary navigation"]');
  const content = document.querySelector('main.content');
  if (!nav || !content || document.querySelector('[data-view="crm"]')) return;

  const mobileMenu = document.querySelector('#mobile-menu');
  if (mobileMenu && !document.querySelector('.workforce-mascot')) {
    const mascot = document.createElement('span');
    mascot.className = 'workforce-mascot';
    mascot.setAttribute('role', 'img');
    mascot.setAttribute('aria-label', 'Workforce mood character');
    mascot.innerHTML = '<span class="mascot-face">🙂</span><span class="mascot-z">Z</span><span class="mascot-z z-two">Z</span><span class="mascot-z z-three">Z</span>';
    mobileMenu.insertAdjacentElement('afterend', mascot);
    const updateMascotMood = () => {
      mascot.querySelector('.mascot-face').textContent = document.body.classList.contains('dark') ? '😴' : '🙂';
    };
    updateMascotMood();
    new MutationObserver(updateMascotMood).observe(document.body, { attributes: true, attributeFilter: ['class'] });
  }

  const navButton = document.createElement('button');
  navButton.type = 'button';
  navButton.dataset.view = 'crm';
  navButton.innerHTML = '<span class="nav-icon">◈</span>CRM';
  nav.appendChild(navButton);

  const view = document.createElement('section');
  view.className = 'view';
  view.id = 'view-crm';
  view.innerHTML = `
    <div class="hero"><div><div class="eyebrow">Customer relationships</div><h1>CRM</h1><p>Manage real companies, prospects, and leads connected to your workforce.</p></div></div>
    <form class="panel crm-form" id="crm-form">
      <input name="company" placeholder="Company name" required>
      <select name="record_type" aria-label="Record type"><option value="company">Company</option><option value="prospect">Prospect</option><option value="lead">Lead</option><option value="client">Client</option></select>
      <input name="industry" placeholder="Industry (optional)">
      <input name="phone" placeholder="Public phone (optional)">
      <input name="email" type="email" placeholder="Public email (optional)">
      <button class="primary" type="submit">Add record</button>
    </form>
    <div class="section-head"><h2>Records</h2><span class="date" id="crm-count"></span></div>
    <form class="panel crm-form" id="crm-file-form">
      <select name="record_id" id="crm-file-record" required><option value="">Choose a CRM record</option></select>
      <input name="file" type="file" accept=".csv,.tsv,.xlsx,.xls,.ods,.pdf,.doc,.docx,.txt,.md,.json,.xml,.html,.png,.jpg,.jpeg,.webp" required>
      <button class="primary" type="submit">Upload file</button>
    </form>
    <div class="panel crm-table" id="crm-records"><div class="empty">Loading CRM records...</div></div>
  `;
  content.appendChild(view);

  const recordsNode = view.querySelector('#crm-records');
  const countNode = view.querySelector('#crm-count');
  const fileRecordNode = view.querySelector('#crm-file-record');
  const render = (records) => {
    countNode.textContent = `${records.length} record${records.length === 1 ? '' : 's'}`;
    fileRecordNode.innerHTML = '<option value="">Choose a CRM record</option>' + records.map((record) => `<option value="${escapeHtml(record.record_id)}">${escapeHtml(record.company)}</option>`).join('');
    if (!records.length) {
      recordsNode.innerHTML = '<div class="empty">No CRM records yet. Add a company, prospect, lead, or client above.</div>';
      return;
    }
    recordsNode.innerHTML = `
      <div class="crm-row header"><span>Company</span><span>Type</span><span>Contact</span><span>Phone</span><span>Status / source</span><span>Actions</span></div>
      ${records.map((record) => `<div class="crm-row"><span class="crm-company">${escapeHtml(record.company)}</span><span>${escapeHtml(record.record_type)}</span><span>${escapeHtml(record.contact_name || record.email || '—')}</span><span>${escapeHtml(record.phone || 'Not verified')}</span><span><div>${escapeHtml(record.status)}</div><div class="task-meta">${escapeHtml(record.source || 'Unknown source')}</div></span><span class="crm-actions"><button class="crm-action" data-crm-edit="${escapeHtml(record.record_id)}">Edit</button><button class="crm-action delete" data-crm-delete="${escapeHtml(record.record_id)}">Delete</button></span></div>`).join('')}
    `;
  };

  const load = async () => {
    recordsNode.innerHTML = '<div class="empty">Loading CRM records...</div>';
    const response = await fetch('/api/crm', { cache: 'no-store' });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || 'CRM API failed to load.');
    render(payload.records || []);
  };

  view.querySelector('#crm-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const button = form.querySelector('button');
    button.disabled = true;
    try {
      const response = await fetch('/api/crm', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(Object.fromEntries(new FormData(form)))
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.error || 'CRM record could not be saved.');
      form.reset();
      await load();
    } catch (error) {
      recordsNode.innerHTML = `<div class="empty">${escapeHtml(error.message)}</div>`;
    } finally {
      button.disabled = false;
    }
  });

  view.querySelector('#crm-file-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const file = form.elements.file.files[0];
    if (!file) return;
    const button = form.querySelector('button');
    button.disabled = true;
    try {
      const contentBase64 = await new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(String(reader.result).split(',')[1] || '');
        reader.onerror = () => reject(new Error('Could not read the selected file.'));
        reader.readAsDataURL(file);
      });
      const response = await fetch(`/api/crm/${encodeURIComponent(form.elements.record_id.value)}/files`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filename: file.name, content_base64: contentBase64 })
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.error || 'File upload failed.');
      form.reset();
      await load();
    } catch (error) {
      recordsNode.innerHTML = `<div class="empty">${escapeHtml(error.message)}</div>`;
    } finally {
      button.disabled = false;
    }
  });

  view.addEventListener('click', async (event) => {
    const editButton = event.target.closest('[data-crm-edit]');
    const deleteButton = event.target.closest('[data-crm-delete]');
    if (!editButton && !deleteButton) return;
    const recordId = (editButton || deleteButton).dataset.crmEdit || deleteButton.dataset.crmDelete;
    const record = (await fetch(`/api/crm/${encodeURIComponent(recordId)}`, { cache: 'no-store' })).json();
    const payload = await record;
    if (deleteButton) {
      if (!window.confirm(`Delete ${payload.record.company}? This cannot be undone.`)) return;
      const response = await fetch(`/api/crm/${encodeURIComponent(recordId)}`, { method: 'DELETE' });
      if (!response.ok) throw new Error('CRM record could not be deleted.');
      await load();
      return;
    }
    const company = window.prompt('Company name', payload.record.company);
    if (company === null) return;
    const industry = window.prompt('Industry', payload.record.industry || '');
    if (industry === null) return;
    const phone = window.prompt('Public phone', payload.record.phone || '');
    if (phone === null) return;
    const response = await fetch(`/api/crm/${encodeURIComponent(recordId)}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ company, industry, phone })
    });
    if (!response.ok) throw new Error('CRM record could not be updated.');
    await load();
  });

  load().catch((error) => {
    recordsNode.innerHTML = `<div class="empty">${escapeHtml(error.message)}</div>`;
  });
})();
