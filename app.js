//app.js
// --- AUTH CHECK ---
if (window.location.pathname.indexOf('login.html') === -1) {
    if (localStorage.getItem('logitrack_session') !== 'active') {
        window.location.href = 'login.html';
    }
}

// --- DATA PERSISTENCE ---
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
    if(d) return JSON.parse(d);
    
    // First time load
    localStorage.setItem('logitrack_data', JSON.stringify(DEFAULT_DATA));
    return DEFAULT_DATA;
}

function saveLogiData(data) {
    localStorage.setItem('logitrack_data', JSON.stringify(data));
}

function logout() {
    localStorage.removeItem('logitrack_session');
    window.location.href = 'login.html';
}

document.addEventListener('DOMContentLoaded', () => {
    initCharts();

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

// Global Modal Handlers
function openModal(id) {
    const m = document.getElementById(id);
    if (m) m.classList.add('active');
}

function closeModal(id) {
    const m = document.getElementById(id);
    if (m) m.classList.remove('active');
}

// Attach globally just in case inline handlers complain about scope
window.openModal = openModal;
window.closeModal = closeModal;

// Close Modal on outside click
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal-overlay')) {
        e.target.classList.remove('active');
    }
});

function initCharts() {
    const volCtx = document.getElementById('volumeChart');
    const statusCtx = document.getElementById('statusChart');

    const appData = getLogiData();
    const encData = appData.encomendas;

    if (volCtx && typeof Chart !== 'undefined') {
        const historyData = [150, 230, 224, 218, 305, 120, encData.length * 10]; // last day gets dynamic volume
        
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
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    }

    if (statusCtx && typeof Chart !== 'undefined') {
        // Calculate real status from data
        let stats = { 'Entregue': 0, 'Na Distribuição': 0, 'Pendente': 0, 'Cancelada': 0 };
        encData.forEach(e => {
            if(stats[e.estado] !== undefined) stats[e.estado]++;
        });

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
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
}

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
