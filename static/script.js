/* ─── Tab switching ─────────────────────────────── */
function switchTab(tab) {
  ['add', 'search', 'library'].forEach(t => {
    document.getElementById(`panel-${t}`).classList.add('hidden');
    document.getElementById(`tab-${t}`).classList.remove('active');
  });
  document.getElementById(`panel-${tab}`).classList.remove('hidden');
  document.getElementById(`tab-${tab}`).classList.add('active');

  // Auto-load library when switching to that tab
  if (tab === 'library') loadLibrary();
}

/* ─── Toast notification ────────────────────────── */
function showToast(msg, type = 'success') {
  const toast = document.getElementById('toast');
  toast.textContent = msg;
  toast.className = `toast ${type} show`;
  setTimeout(() => { toast.className = 'toast'; }, 2800);
}

/* ─── Add Song ──────────────────────────────────── */
function addSong() {
  const titleEl = document.getElementById('title');
  const artistEl = document.getElementById('artist');
  const urlEl = document.getElementById('url');

  if (!titleEl.value.trim() || !artistEl.value.trim() || !urlEl.value.trim()) {
    showToast('Please fill in all fields.', 'error');
    return;
  }

  const btn = document.getElementById('add-song-btn');
  btn.disabled = true;
  btn.textContent = 'Adding…';

  fetch('/add_song', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      title: titleEl.value.trim(),
      artist: artistEl.value.trim(),
      url: urlEl.value.trim()
    })
  })
    .then(res => res.json())
    .then(d => {
      showToast('✓ ' + d.message, 'success');
      titleEl.value = '';
      artistEl.value = '';
      urlEl.value = '';
      // Switch to library so user can see their new song
      switchTab('library');
    })
    .catch(() => showToast('Failed to add song.', 'error'))
    .finally(() => {
      btn.disabled = false;
      btn.innerHTML = '<span class="btn-icon">＋</span> Add to Library';
    });
}

/* ─── Search ────────────────────────────────────── */
function searchSong() {
  const q = document.getElementById('search').value.trim();
  const btn = document.getElementById('search-btn');
  const resultDiv = document.getElementById('result');

  if (!q) { showToast('Enter something to search.', 'error'); return; }

  btn.disabled = true;
  btn.textContent = '…';
  resultDiv.innerHTML = '';

  fetch(`/search?q=${encodeURIComponent(q)}`)
    .then(res => res.json())
    .then(data => {
      if (data.length === 0) {
        resultDiv.innerHTML = `
        <div class="empty-state">
          <div class="es-icon">🔇</div>
          <p>No songs found for "<strong>${escHtml(q)}</strong>"</p>
        </div>`;
        return;
      }
      data.forEach(song => {
        resultDiv.appendChild(buildSongCard(song, true));
      });
    })
    .catch(() => showToast('Search failed.', 'error'))
    .finally(() => { btn.disabled = false; btn.textContent = 'Search'; });
}

/* ─── Library ───────────────────────────────────── */
function loadLibrary() {
  const libraryDiv = document.getElementById('library');
  libraryDiv.innerHTML = `<div class="empty-state"><div class="es-icon">⏳</div><p>Loading…</p></div>`;

  fetch('/library')
    .then(res => res.json())
    .then(data => {
      libraryDiv.innerHTML = '';

      // Update count badge
      const badge = document.getElementById('library-count');
      if (badge) badge.textContent = data.length;

      if (data.length === 0) {
        libraryDiv.innerHTML = `
        <div class="empty-state">
          <div class="es-icon">🎵</div>
          <p>Your library is empty.<br>Add a song to get started!</p>
        </div>`;
        return;
      }
      data.forEach(song => {
        libraryDiv.appendChild(buildSongCard(song, false));
      });
    })
    .catch(() => showToast('Could not load library.', 'error'));
}

/* ─── Build song card ───────────────────────────── */
function buildSongCard(song, showFav = false) {
  const div = document.createElement('div');
  div.className = 'song-card';
  div.setAttribute('data-id', song.id);

  // Get YouTube thumbnail if possible
  let thumbHtml = '<span style="font-size:1.3rem">🎵</span>';
  const vid = extractYouTubeId(song.url || '');
  if (vid) {
    thumbHtml = `<img src="https://img.youtube.com/vi/${vid}/default.jpg" alt="" loading="lazy" />`;
  }

  const favBtn = showFav
    ? `<button class="btn-icon-sm fav-btn" title="Save to Library" onclick="fav(${song.id}, this)">
        ${song.fav ? '✅' : '♡'}
       </button>`
    : '';

  div.innerHTML = `
    <div class="song-thumb">${thumbHtml}</div>
    <div class="song-info">
      <div class="song-title">${escHtml(song.title)}</div>
      <div class="song-artist">${escHtml(song.artist || '—')}</div>
    </div>
    <div class="song-actions">
      <button class="btn-icon-sm play-btn" title="Play"
        onclick="playYouTube('${escAttr(song.url)}', '${escAttr(song.title)}', '${escAttr(song.artist || '')}')">▶</button>
      ${favBtn}
    </div>
  `;
  return div;
}

/* ─── Play YouTube ──────────────────────────────── */
function playYouTube(link, title = '', artist = '') {
  if (!link) { showToast('No YouTube link found.', 'error'); return; }

  const videoId = extractYouTubeId(link.trim());
  if (!videoId) { showToast('Invalid YouTube link.', 'error'); return; }

  document.getElementById('ytplayer').src =
    `https://www.youtube.com/embed/${videoId}?autoplay=1`;

  // Update now-playing info
  const info = document.getElementById('now-playing-info');
  if (title) {
    document.getElementById('np-title').textContent = title;
    document.getElementById('np-artist').textContent = artist || '—';
    info.classList.remove('hidden');

    // Replace art placeholder with thumbnail
    document.getElementById('player-art').innerHTML =
      `<img src="https://img.youtube.com/vi/${videoId}/hqdefault.jpg"
            alt="${escHtml(title)}"
            style="width:100%;height:100%;object-fit:cover;" />`;
  }

  // Start player bar animation
  const fill = document.getElementById('player-bar-fill');
  if (fill) fill.classList.remove('idle');
}

/* ─── Add to Favourites ─────────────────────────── */
function fav(id, btn) {
  if (btn) { btn.disabled = true; btn.textContent = '✅'; }
  fetch(`/favorite/${id}`)
    .then(() => showToast('♥ Marked as favourite!', 'success'))
    .catch(() => {
      showToast('Failed.', 'error');
      if (btn) { btn.disabled = false; btn.textContent = '♡'; }
    });
}

/* ─── Extract YouTube ID ─────────────────────────── */
function extractYouTubeId(link) {
  if (!link) return '';
  if (link.includes('watch?v=')) return link.split('watch?v=')[1].split('&')[0];
  if (link.includes('youtu.be/')) return link.split('youtu.be/')[1].split('?')[0];
  if (link.includes('youtube.com/shorts/')) return link.split('youtube.com/shorts/')[1].split('?')[0];
  return '';
}

/* ─── Helpers ───────────────────────────────────── */
function escHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
function escAttr(s) {
  return String(s).replace(/'/g, "\\'");
}
// DELETE a song
async function deleteSong(id) {
  if (!confirm("Delete this song?")) return;
  const res = await fetch(`/delete/${id}`, { method: "DELETE" });
  const data = await res.json();
  alert(data.message);
  loadLibrary(); // refresh the list
}

// Open edit form pre-filled with current song data
function openEditModal(id, title, artist, url) {
  document.getElementById("edit-id").value = id;
  document.getElementById("edit-title").value = title;
  document.getElementById("edit-artist").value = artist;
  document.getElementById("edit-url").value = url;
  document.getElementById("edit-modal").style.display = "flex";
}

function closeEditModal() {
  document.getElementById("edit-modal").style.display = "none";
}

// SUBMIT the update
async function submitUpdate() {
  const id = document.getElementById("edit-id").value;
  const title = document.getElementById("edit-title").value;
  const artist = document.getElementById("edit-artist").value;
  const url = document.getElementById("edit-url").value;

  const res = await fetch(`/update/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, artist, url })
  });
  const data = await res.json();
  alert(data.message);
  closeEditModal();
  loadLibrary(); // refresh the list
}