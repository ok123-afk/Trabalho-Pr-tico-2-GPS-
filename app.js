//app.js

// ─── AUTH CHECK ───────────────────────────────────────────────────────────────
if (window.location.pathname.indexOf('login.html') === -1) {
    if (localStorage.getItem('logitrack_session') !== 'active') {
        window.location.href = 'login.html';
    }
}

// ─── RBAC DEFINITIONS ─────────────────────────────────────────────────────────
// Define which nav hrefs are accessible per role
const ROLE_NAV_ACCESS = {
    admin: ['index.html', 'clientes.html', 'encomendas.html', 'entregas.html', 'estafetas.html', 'recursos.html', 'comunicacao.html'],
    gestor: ['index.html', 'clientes.html', 'encomendas.html', 'entregas.html', 'recursos.html', 'comunicacao.html'],
    staff:  ['index.html', 'clientes.html', 'encomendas.html', 'entregas.html', 'recursos.html', 'comunicacao.html'],
    cliente: ['encomendas.html', 'comunicacao.html']
};

// Pages that each role lands on if they try to access a restricted page
const ROLE_HOME = {
    admin: 'index.html',
    gestor: 'index.html',
    staff: 'index.html',
    cliente: 'encomendas.html'
};

// ─── USER SESSION ─────────────────────────────────────────────────────────────
function getCurrentUser() {
    const raw = localStorage.getItem('logitrack_current_user');
    if (raw) return JSON.parse(raw);
    return { username: 'admin', name: 'Administrador', email: 'admin@logitrack.pt', role: 'admin' };
}

function getUserInitials(name) {
    return name.split(' ').map(p => p[0]).slice(0, 2).join('').toUpperCase();
}

// ─── DATA PERSISTENCE ─────────────────────────────────────────────────────────
const DEFAULT_DATA = {
    clientes: [
        { nome: 'Maria João Silva', tipo: 'Particular', email: 'maria.silva@email.com', encomendas: 2 },
        { nome: 'TechStore Lda', tipo: 'Empresa', email: 'logistica@techstore.pt', encomendas: 14 },
        { nome: 'Rui Pereira', tipo: 'Particular', email: 'rui.p@email.com', encomendas: 0 },
        { nome: 'Mercado Fio Unipessoal', tipo: 'Empresa', email: 'geral@mercadofio.pt', encomendas: 6 }
    ],
    encomendas: [
        { id: '#10023', cliente: 'TechStore Lda', destino: 'Lisboa (Centro)', data: 'Hoje, 10:45', estado: 'Na Distribuição' },
        { id: '#10024', cliente: 'Maria João Silva', destino: 'Amadora', data: 'Hoje, 11:20', estado: 'Pendente' },
        { id: '#10022', cliente: 'Rui Pereira', destino: 'Cascais', data: 'Hoje, 09:15', estado: 'Entregue' },
        { id: '#10020', cliente: 'Mercado Fio Unipessoal', destino: 'Sintra', data: 'Ontem, 16:30', estado: 'Cancelada' }
    ]
};

function getLogiData() {
    const d = localStorage.getItem('logitrack_data');
    if (d) return JSON.parse(d);
    localStorage.setItem('logitrack_data', JSON.stringify(DEFAULT_DATA));
    return DEFAULT_DATA;
}

function saveLogiData(data) {
    localStorage.setItem('logitrack_data', JSON.stringify(data));
}

function logout() {
    localStorage.removeItem('logitrack_session');
    localStorage.removeItem('logitrack_current_user');
    window.location.href = 'login.html';
}

// ─── RBAC: Apply nav visibility & page access control ─────────────────────────
function applyRBAC() {
    const user = getCurrentUser();
    const role = user.role || 'cliente';
    const allowed = ROLE_NAV_ACCESS[role] || ROLE_NAV_ACCESS['cliente'];
    const home = ROLE_HOME[role] || 'encomendas.html';

    // Page-level access guard: redirect if current page is not allowed
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    if (currentPage !== 'login.html' && !allowed.includes(currentPage)) {
        window.location.href = home;
        return;
    }

    // Hide nav items the user doesn't have access to
    document.querySelectorAll('.nav-item').forEach(item => {
        const href = item.getAttribute('href');
        if (href && !allowed.includes(href)) {
            item.style.display = 'none';
        } else {
            item.style.display = '';
        }
    });

    // Show/hide admin-only elements
    document.querySelectorAll('[data-admin-only]').forEach(el => {
        el.style.display = (role === 'admin') ? '' : 'none';
    });

    // Show role badge in navbar if element exists
    const roleBadge = document.getElementById('nav-role-badge');
    if (roleBadge) {
        const roleConfig = {
            admin:    { label: 'Admin',    color: '#4318ff', bg: 'rgba(67,24,255,0.12)' },
            gestor:   { label: 'Gestor',   color: '#05cd99', bg: 'rgba(5,205,153,0.12)' },
            staff:    { label: 'Staff',    color: '#05cd99', bg: 'rgba(5,205,153,0.12)' },
            cliente:  { label: 'Cliente',  color: '#ee5d50', bg: 'rgba(238,93,80,0.12)' }
        };
        const cfg = roleConfig[role] || roleConfig['cliente'];
        roleBadge.textContent = cfg.label;
        roleBadge.style.cssText = `
            display: inline-flex; align-items: center;
            padding: 3px 10px; border-radius: 20px;
            font-size: 11px; font-weight: 700; letter-spacing: 0.5px;
            text-transform: uppercase; color: ${cfg.color};
            background: ${cfg.bg}; border: 1px solid ${cfg.color}33;
        `;
    }
}

// ─── NAVBAR USER INFO INJECTION ───────────────────────────────────────────────
function injectNavUser() {
    const user = getCurrentUser();
    const avatarEl = document.getElementById('nav-user-avatar');
    const nameEl = document.getElementById('nav-user-name');
    const roleEl = document.getElementById('nav-user-role');

    if (avatarEl) {
        if (avatarEl.tagName === 'IMG') {
            const span = document.createElement('span');
            span.id = 'nav-user-avatar';
            span.style.cssText = 'width:32px;height:32px;border-radius:50%;background:#4318ff;color:#fff;font-size:13px;font-weight:700;display:flex;align-items:center;justify-content:center;border:2px solid #4318ff;flex-shrink:0;';
            span.textContent = getUserInitials(user.name);
            avatarEl.replaceWith(span);
        } else {
            avatarEl.textContent = getUserInitials(user.name);
        }
    }
    if (nameEl) nameEl.textContent = user.name;
    if (roleEl) {
        const roleMap = { admin: 'Administrador', gestor: 'Gestor', staff: 'Staff', cliente: 'Cliente' };
        roleEl.textContent = roleMap[user.role] || user.role;
    }
}

// ─── DOM READY ────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    // Apply RBAC first (may redirect)
    applyRBAC();

    // Inject user info
    injectNavUser();

    // Charts
    initCharts();

    // Notifications button
    const notifBtn = document.getElementById('notifications-btn');
    if (notifBtn) {
        notifBtn.addEventListener('click', () => {
            showSimulatedToast("Você tem 3 novas notificações não lidas no sistema.");
        });
    }

    // Set active navbar item
    const currentPath = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.nav-item').forEach(item => {
        const h = item.getAttribute('href');
        if (h === currentPath) item.classList.add('active');
    });

    // Global Search Logic
    const searchInput = document.querySelector('.search-bar input');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase();
            document.querySelectorAll('.data-table tbody tr').forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(query) ? '' : 'none';
            });
        });
    }
});

// ─── GLOBAL MODAL HANDLERS ────────────────────────────────────────────────────
function openModal(id) {
    const m = document.getElementById(id);
    if (m) m.classList.add('active');
}

function closeModal(id) {
    const m = document.getElementById(id);
    if (m) m.classList.remove('active');
}

window.openModal = openModal;
window.closeModal = closeModal;

document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal-overlay')) {
        e.target.classList.remove('active');
    }
});

// ─── CHARTS ───────────────────────────────────────────────────────────────────
function initCharts() {
    const volCtx = document.getElementById('volumeChart');
    const statusCtx = document.getElementById('statusChart');

    const appData = getLogiData();
    const encData = appData.encomendas;

    if (volCtx && typeof Chart !== 'undefined') {
        const historyData = [150, 230, 224, 218, 305, 120, encData.length * 10];

        new Chart(volCtx, {
            type: 'bar',
            data: {
                labels: ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Hoje'],
                datasets: [{
                    label: 'Encomendas Recebidas',
                    data: historyData,
                    backgroundColor: 'rgba(67, 24, 255, 0.85)',
                    borderRadius: 6,
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: { y: { beginAtZero: true } }
            }
        });
    }

    if (statusCtx && typeof Chart !== 'undefined') {
        let stats = { 'Entregue': 0, 'Na Distribuição': 0, 'Pendente': 0, 'Cancelada': 0 };
        encData.forEach(e => { if (stats[e.estado] !== undefined) stats[e.estado]++; });

        new Chart(statusCtx, {
            type: 'doughnut',
            data: {
                labels: ['Entregue', 'Na Distribuição', 'Pendente', 'Cancelada'],
                datasets: [{
                    data: [stats['Entregue'], stats['Na Distribuição'], stats['Pendente'], stats['Cancelada']],
                    backgroundColor: ['#05cd99', '#4318ff', '#ffce20', '#ee5d50'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: 'bottom' } }
            }
        });
    }
}

// ─── TOAST ────────────────────────────────────────────────────────────────────
function showSimulatedToast(msg) {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<i class="fa-solid fa-circle-info" style="color: var(--accent-color); font-size: 20px;"></i> <div>${msg}</div>`;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'fadeOut 0.3s ease forwards';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function simulateClientComms() {
    showSimulatedToast("A enviar SMS e Email ao cliente...");
    setTimeout(() => {
        showSimulatedToast("Comunicação entregue com sucesso! (Req. 4.8)");
    }, 1500);
}