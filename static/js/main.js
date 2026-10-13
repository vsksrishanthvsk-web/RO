/**
 * Rasoi Restaurant Client-Side Interactions
 */

// Helper to get CSRF token from cookies or DOM
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrftoken = getCookie('csrftoken') || (document.querySelector('[name=csrfmiddlewaretoken]')?.value || '');

// Toast Notification
function showToast(message, type = 'success') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'messages-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `<span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// Add to Cart via AJAX
function setupAddToCart() {
  const addButtons = document.querySelectorAll('.js-add-to-cart');
  addButtons.forEach(button => {
    button.addEventListener('click', async (e) => {
      e.preventDefault();
      const itemId = button.dataset.itemId;
      const itemName = button.dataset.itemName;
      const originalHtml = button.innerHTML;

      button.disabled = true;
      button.innerHTML = '<span>Adding…</span>';

      try {
        const response = await fetch('/cart/add/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
          },
          body: JSON.stringify({ item_id: itemId, quantity: 1 })
        });

        const data = await response.json();
        if (data.success) {
          // Update cart badges in header
          const badges = document.querySelectorAll('.js-cart-count');
          badges.forEach(b => {
            b.textContent = data.cart_count;
            b.style.display = data.cart_count > 0 ? 'flex' : 'none';
          });

          showToast(`Added ${itemName} to your table order!`, 'success');

          button.innerHTML = '<span>✓ Added</span>';
          setTimeout(() => {
            button.innerHTML = originalHtml;
            button.disabled = false;
          }, 1200);
        } else {
          showToast('Could not add item to cart', 'error');
          button.innerHTML = originalHtml;
          button.disabled = false;
        }
      } catch (err) {
        console.error(err);
        showToast('Error adding item', 'error');
        button.innerHTML = originalHtml;
        button.disabled = false;
      }
    });
  });
}

// Order Status Polling (for /track/<order_code>/)
function setupTrackingPolling() {
  const tracker = document.querySelector('.js-order-tracker');
  if (!tracker) return;

  const orderCode = tracker.dataset.orderCode;
  if (!orderCode) return;

  const statusDisplayEl = document.getElementById('tracker-status-text');
  const progressBarEl = document.getElementById('timeline-bar');
  const steps = document.querySelectorAll('.timeline-step');

  const pollInterval = setInterval(async () => {
    try {
      const res = await fetch(`/api/status/${orderCode}/`);
      if (res.ok) {
        const data = await res.json();
        
        if (statusDisplayEl) {
          statusDisplayEl.textContent = data.status_display;
        }

        // Update step UI
        const stepNum = data.step_number;
        if (progressBarEl) {
          const widthPct = stepNum === 1 ? '10%' : stepNum === 2 ? '40%' : stepNum === 3 ? '70%' : '95%';
          progressBarEl.style.width = widthPct;
        }

        steps.forEach((step, idx) => {
          const stepIndex = idx + 1;
          step.classList.remove('completed', 'current');
          if (stepIndex < stepNum) {
            step.classList.add('completed');
          } else if (stepIndex === stepNum) {
            step.classList.add('current');
          }
        });

        if (data.status === 'SERVED' || data.status === 'CANCELLED') {
          clearInterval(pollInterval);
        }
      }
    } catch (e) {
      console.error("Polling error", e);
    }
  }, 4000);
}

// Kitchen KDS auto-refresh every 7 seconds
function setupKitchenAutoRefresh() {
  const kds = document.querySelector('.js-kitchen-screen');
  if (!kds) return;

  // Status transitions
  document.querySelectorAll('.js-status-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      const orderCode = btn.dataset.orderCode;
      const targetStatus = btn.dataset.status;

      try {
        const res = await fetch(`/kitchen/update/${orderCode}/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest'
          },
          body: JSON.stringify({ status: targetStatus })
        });
        const data = await res.json();
        if (data.success) {
          window.location.reload();
        }
      } catch (err) {
        console.error(err);
      }
    });
  });

  // Auto reload every 8s if no forms are focused
  setInterval(() => {
    if (!document.activeElement || document.activeElement.tagName === 'BODY') {
      window.location.reload();
    }
  }, 8000);
}

document.addEventListener('DOMContentLoaded', () => {
  setupAddToCart();
  setupTrackingPolling();
  setupKitchenAutoRefresh();
});
