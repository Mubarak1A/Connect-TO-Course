/* Connect to Course — Interactive UI & Live Updates */

// Toast notification helper
function showToast(message, type = 'success') {
  const container = document.getElementById('toast-container') || createToastContainer();
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <span>${message}</span>
    <i class="fas fa-times" style="cursor:pointer;" onclick="this.parentElement.remove()"></i>
  `;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(40px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

function createToastContainer() {
  const container = document.createElement('div');
  container.id = 'toast-container';
  container.className = 'toast-container';
  document.body.appendChild(container);
  return container;
}

// Auto dismiss initial server-rendered toasts
document.addEventListener('DOMContentLoaded', () => {
  const existingToasts = document.querySelectorAll('.toast');
  existingToasts.forEach((toast) => {
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(40px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 4000);
  });
});

// Modal helpers
function openModal(id) {
  const modal = document.getElementById(id);
  if (modal) modal.style.display = 'flex';
}

function closeModal(id) {
  const modal = document.getElementById(id);
  if (modal) modal.style.display = 'none';
}

function switchModal(fromId, toId) {
  closeModal(fromId);
  openModal(toId);
}

// Close modals when clicking outside
window.addEventListener('click', (e) => {
  if (e.target.classList.contains('modal-overlay')) {
    e.target.style.display = 'none';
  }
});

// Bookmark drawer toggle
let drawerOpen = false;
function toggleDrawer() {
  if (drawerOpen) closeDrawer();
  else openDrawer();
}

function openDrawer() {
  const drawer = document.getElementById('bookmark_drawer');
  if (drawer) {
    drawer.style.width = window.innerWidth < 480 ? '100%' : '340px';
    drawerOpen = true;
  }
}

function closeDrawer() {
  const drawer = document.getElementById('bookmark_drawer');
  if (drawer) {
    drawer.style.width = '0px';
    drawerOpen = false;
  }
}

// Live Bookmark (Save) Action
function saveCourse(button, courseId, title, instructor, url) {
  // If user is not logged in, prompt signup
  const bookmarkCountBadge = document.getElementById('nav-bookmark-count');
  if (!bookmarkCountBadge) {
    showToast('Please log in or sign up to save courses!', 'warning');
    openModal('signup-modal');
    return;
  }

  const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');

  // Optimistic UI update on button
  button.classList.add('saved');
  button.innerHTML = '<i class="fas fa-check"></i> Saved';
  button.disabled = true;

  fetch('/save', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken || ''
    },
    body: JSON.stringify({ id: courseId })
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.status === 'success') {
        showToast('Course added to bookmarks!', 'success');
        updateBookmarkCount(data.bookmark_count);
        addBookmarkToDrawer(courseId, title, instructor, url);
      } else {
        showToast(data.message || 'Could not bookmark course', 'danger');
        button.classList.remove('saved');
        button.innerHTML = '<i class="far fa-bookmark"></i> Save';
        button.disabled = false;
      }
    })
    .catch((err) => {
      console.error(err);
      showToast('Network error while saving course', 'danger');
      button.classList.remove('saved');
      button.innerHTML = '<i class="far fa-bookmark"></i> Save';
      button.disabled = false;
    });
}

// Live Delete Bookmark Action
function deleteBookmark(courseId) {
  const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');

  const drawerItem = document.getElementById(`drawer-item-${courseId}`);
  if (drawerItem) {
    drawerItem.style.opacity = '0.4';
  }

  fetch('/delete', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken || ''
    },
    body: JSON.stringify({ id: courseId })
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.status === 'success') {
        showToast('Bookmark removed', 'warning');
        updateBookmarkCount(data.bookmark_count);

        // Animate remove from drawer
        if (drawerItem) {
          drawerItem.style.transition = 'all 0.25s ease';
          drawerItem.style.transform = 'translateX(-30px)';
          drawerItem.style.opacity = '0';
          setTimeout(() => {
            drawerItem.remove();
            checkDrawerEmpty();
          }, 250);
        }

        // Also update any save button currently visible on the page
        const saveBtn = document.querySelector(`.btn-save[data-id="${courseId}"]`);
        if (saveBtn) {
          saveBtn.classList.remove('saved');
          saveBtn.innerHTML = '<i class="far fa-bookmark"></i> Save';
          saveBtn.disabled = false;
        }
      } else {
        showToast(data.message || 'Failed to remove bookmark', 'danger');
        if (drawerItem) drawerItem.style.opacity = '1';
      }
    })
    .catch((err) => {
      console.error(err);
      showToast('Network error while removing bookmark', 'danger');
      if (drawerItem) drawerItem.style.opacity = '1';
    });
}

// Helpers for live DOM updates in Drawer
function updateBookmarkCount(count) {
  const badge = document.getElementById('nav-bookmark-count');
  if (badge) badge.innerText = count;
}

function addBookmarkToDrawer(id, title, instructor, url) {
  const list = document.getElementById('drawer-bookmarks-list');
  if (!list) return;

  const emptyMsg = document.getElementById('drawer-empty-msg');
  if (emptyMsg) emptyMsg.remove();

  if (document.getElementById(`drawer-item-${id}`)) return; // already in drawer

  const item = document.createElement('div');
  item.className = 'bookmark-item';
  item.id = `drawer-item-${id}`;
  item.style.animation = 'slideIn 0.2s ease-out';
  item.innerHTML = `
    <a href="${url}" target="_blank" class="bookmark-item-title">${escapeHtml(title)}</a>
    <div class="bookmark-item-instructor">By ${escapeHtml(instructor)}</div>
    <button class="bookmark-item-delete" title="Remove bookmark" onclick="deleteBookmark('${id}')">
      <i class="fas fa-trash-alt"></i>
    </button>
  `;
  list.prepend(item);
}

function checkDrawerEmpty() {
  const list = document.getElementById('drawer-bookmarks-list');
  if (list && list.children.length === 0) {
    list.innerHTML = `
      <div class="bookmark-empty" id="drawer-empty-msg">
        <i class="far fa-bookmark"></i>
        <p>No bookmarked courses yet.</p>
        <p style="font-size:0.75rem; margin-top:4px;">Click Save on any course to add it here!</p>
      </div>
    `;
  }
}

function escapeHtml(str) {
  if (!str) return '';
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

// Live Search with Debounce
let searchTimeout = null;
function handleSearchInput(query) {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    performSearch(query.trim());
  }, 250);
}

function performSearch(query) {
  const resultsContainer = document.getElementById('search-results');
  const resultsSection = document.getElementById('search-results-section');
  if (!resultsContainer) return;

  if (!query) {
    if (resultsSection) resultsSection.style.display = 'none';
    resultsContainer.innerHTML = '';
    return;
  }

  if (resultsSection) resultsSection.style.display = 'block';
  resultsContainer.innerHTML = `
    <div class="empty-state" style="grid-column: 1 / -1;">
      <i class="fas fa-spinner fa-spin" style="font-size:2rem; color:var(--primary);"></i>
      <p style="margin-top:10px;">Searching courses for "${escapeHtml(query)}"...</p>
    </div>
  `;

  fetch(`/search?query=${encodeURIComponent(query)}`)
    .then((res) => res.json())
    .then((data) => {
      const results = data.results || [];
      resultsContainer.innerHTML = '';

      if (results.length === 0) {
        resultsContainer.innerHTML = `
          <div class="empty-state" style="grid-column: 1 / -1;">
            <i class="fas fa-search"></i>
            <h3>No courses found</h3>
            <p>We couldn't find any courses matching "${escapeHtml(query)}". Try another keyword!</p>
          </div>
        `;
        return;
      }

      results.forEach((course) => {
        const card = document.createElement('div');
        card.className = 'course-card';
        card.innerHTML = `
          <div class="course-thumb-wrap">
            <img class="course-thumb" src="/static/images/img2.png" alt="Course thumbnail">
            <span class="course-platform-badge">Udemy</span>
          </div>
          <div class="course-body">
            <h3 class="course-title" title="${escapeHtml(course.title)}">${escapeHtml(course.title)}</h3>
            <p class="course-instructor">Instructor: ${escapeHtml(course.instructor)}</p>
            <div class="course-footer">
              <a href="${course.url}" target="_blank" class="btn-view">
                <i class="fas fa-external-link-alt"></i> View Course
              </a>
              <button class="btn-save" data-id="${course.id}"
                onclick="saveCourse(this, '${course.id}', '${escapeHtml(course.title)}', '${escapeHtml(course.instructor)}', '${course.url}')">
                <i class="far fa-bookmark"></i> Save
              </button>
            </div>
          </div>
        `;
        resultsContainer.appendChild(card);
      });
    })
    .catch((err) => {
      console.error(err);
      resultsContainer.innerHTML = `
        <div class="empty-state" style="grid-column: 1 / -1;">
          <i class="fas fa-exclamation-triangle" style="color:var(--danger);"></i>
          <h3>Search Error</h3>
          <p>Failed to retrieve search results. Please try again.</p>
        </div>
      `;
    });
}
