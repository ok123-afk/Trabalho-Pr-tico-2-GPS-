import os

base_dir = r"c:\Users\admin\Documents\PSW\GPS\poj2_2"

try:
    with open(os.path.join(base_dir, "style.css"), "r", encoding="utf-8") as f:
        css_content = f.read()
except:
    css_content = ""

try:
    with open(os.path.join(base_dir, "app.js"), "r", encoding="utf-8") as f:
        js_content = f.read()
except:
    js_content = ""

pages = {
    "index.html": """
        <div class="view-section active">
            <div class="page-header">
                <h1 class="page-title">Dashboard Operacional</h1>
                <p class="page-subtitle">Ponto de situação do sistema global (Ref: 4.6, 4.7)</p>
            </div>
            <div class="dashboard-grid">
                <div class="stat-card">
                    <div class="stat-icon"><i class="fa-solid fa-box"></i></div>
                    <div class="stat-info">
                        <div class="stat-label">Entregas Hoje</div>
                        <div class="stat-value">1,204</div>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon" style="color: var(--success-color); background-color: rgba(5,205,153,0.1);"><i class="fa-solid fa-check"></i></div>
                    <div class="stat-info">
                        <div class="stat-label">Taxa no Prazo</div>
                        <div class="stat-value">94.2%</div>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon" style="color: var(--warning-color); background-color: rgba(255,206,32,0.1);"><i class="fa-solid fa-clock"></i></div>
                    <div class="stat-info">
                        <div class="stat-label">Tempo Médio</div>
                        <div class="stat-value">38 min</div>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon" style="color: var(--danger-color); background-color: rgba(238,93,80,0.1);"><i class="fa-solid fa-motorcycle"></i></div>
                    <div class="stat-info">
                        <div class="stat-label">Estafetas Ativos</div>
                        <div class="stat-value">45 / 50</div>
                    </div>
                </div>
            </div>
            <div class="panels-grid">
                <div class="panel-card">
                    <div class="panel-header">
                        <h2 class="panel-title">Volume de Encomendas (Últimos 7 Dias)</h2>
                    </div>
                    <div class="chart-container">
                        <canvas id="volumeChart"></canvas>
                    </div>
                </div>
                <div class="panel-card">
                    <div class="panel-header">
                        <h2 class="panel-title">Estado Atual</h2>
                    </div>
                    <div class="chart-container">
                        <canvas id="statusChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
    """,
    "clientes.html": """
        <div class="view-section active">
            <div class="page-header" style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h1 class="page-title">Gestão de Clientes</h1>
                    <p class="page-subtitle">Registo e histórico de clientes (Ref: 4.1)</p>
                </div>
                <button class="btn btn-primary" onclick="openModal('clienteModal')">+ Novo Cliente</button>
            </div>
            <div class="panel-card">
                <div class="table-container">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Nome</th>
                                <th>Tipo</th>
                                <th>Email / Telefone</th>
                                <th>Enc. Ativas</th>
                                <th>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr><td>Maria João Silva</td><td>Particular</td><td>maria.silva@email.com</td><td>2</td><td><button class="btn-icon" onclick="editCliente(this)"><i class="fa-solid fa-pen"></i></button></td></tr>
                            <tr><td>TechStore Lda</td><td>Empresa</td><td>logistica@techstore.pt</td><td>14</td><td><button class="btn-icon" onclick="editCliente(this)"><i class="fa-solid fa-pen"></i></button></td></tr>
                            <tr><td>Rui Pereira</td><td>Particular</td><td>rui.p@email.com</td><td>0</td><td><button class="btn-icon" onclick="editCliente(this)"><i class="fa-solid fa-pen"></i></button></td></tr>
                            <tr><td>Mercado Fio Unipessoal</td><td>Empresa</td><td>geral@mercadofio.pt</td><td>6</td><td><button class="btn-icon" onclick="editCliente(this)"><i class="fa-solid fa-pen"></i></button></td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Modal -->
        <div class="modal-overlay" id="clienteModal">
            <div class="modal">
                <div class="modal-header">
                    <h2 class="modal-title">Novo Cliente</h2>
                    <button type="button" class="close-btn" onclick="resetClienteModal()"><i class="fa-solid fa-xmark"></i></button>
                </div>
                <form id="formCliente" onsubmit="event.preventDefault(); addClienteRow();">
                    <div class="form-group">
                        <label>Nome do Cliente</label>
                        <input type="text" class="form-control" id="cNome" required>
                    </div>
                    <div class="form-group">
                        <label>Email</label>
                        <input type="email" class="form-control" id="cEmail" required>
                    </div>
                    <div class="form-group">
                        <label>Tipo</label>
                        <select class="form-control" id="cTipo">
                            <option>Particular</option>
                            <option>Empresa</option>
                        </select>
                    </div>
                    <button type="submit" class="btn btn-primary" style="width:100%">Guardar Cliente</button>
                </form>
            </div>
        </div>
        <script>
            let editRowCliente = null;
            function editCliente(btn) {
                const tr = btn.closest('tr');
                editRowCliente = tr;
                document.getElementById('cNome').value = tr.cells[0].textContent;
                document.getElementById('cTipo').value = tr.cells[1].textContent;
                document.getElementById('cEmail').value = tr.cells[2].textContent;
                
                document.querySelector('#clienteModal .modal-title').textContent = "Editar Cliente";
                document.querySelector('#formCliente button[type="submit"]').textContent = "Atualizar Cliente";
                openModal('clienteModal');
            }

            function resetClienteModal() {
                closeModal('clienteModal');
                document.getElementById('formCliente').reset();
                editRowCliente = null;
                document.querySelector('#clienteModal .modal-title').textContent = "Novo Cliente";
                document.querySelector('#formCliente button[type="submit"]').textContent = "Guardar Cliente";
            }

            function addClienteRow() {
                const nome = document.getElementById('cNome').value;
                const email = document.getElementById('cEmail').value;
                const tipo = document.getElementById('cTipo').value;
                
                if(editRowCliente) {
                    editRowCliente.cells[0].textContent = nome;
                    editRowCliente.cells[1].textContent = tipo;
                    editRowCliente.cells[2].textContent = email;
                    showSimulatedToast('Cliente atualizado!');
                } else {
                    const tbody = document.querySelector('.data-table tbody');
                    if(!tbody) return;
                    const tr = document.createElement('tr');
                    tr.innerHTML = `<td>${nome}</td><td>${tipo}</td><td>${email}</td><td>0</td><td><button class="btn-icon" onclick="editCliente(this)"><i class="fa-solid fa-pen"></i></button></td>`;
                    tbody.insertBefore(tr, tbody.firstChild);
                    showSimulatedToast('Cliente criado!');
                }
                resetClienteModal();
            }
        </script>
    """,
    "encomendas.html": """
        <div class="view-section active">
            <div class="page-header" style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h1 class="page-title">Gestão de Encomendas</h1>
                    <p class="page-subtitle">Listagem, registo e estado de ordens (Ref: 4.2)</p>
                </div>
                <button class="btn btn-primary" onclick="openModal('encomendaModal')">+ Nova Encomenda</button>
            </div>
            <div class="panel-card">
                <div class="table-container">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Cliente</th>
                                <th>Destino</th>
                                <th>Data</th>
                                <th>Estado</th>
                                <th>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr><td>#10023</td><td>TechStore Lda</td><td>Lisboa (Centro)</td><td>Hoje, 10:45</td><td><span class="status distribuicao">Na Distribuição</span></td><td><button class="btn-icon" onclick="editEncomenda(this)"><i class="fa-solid fa-pen"></i></button></td></tr>
                            <tr><td>#10024</td><td>Maria João Silva</td><td>Amadora</td><td>Hoje, 11:20</td><td><span class="status pendente">Pendente</span></td><td><button class="btn-icon" onclick="editEncomenda(this)"><i class="fa-solid fa-pen"></i></button></td></tr>
                            <tr><td>#10022</td><td>Rui Pereira</td><td>Cascais</td><td>Hoje, 09:15</td><td><span class="status entregue">Entregue</span></td><td><button class="btn-icon" onclick="editEncomenda(this)"><i class="fa-solid fa-pen"></i></button></td></tr>
                            <tr><td>#10020</td><td>Mercado Fio</td><td>Sintra</td><td>Ontem, 16:30</td><td><span class="status cancelada">Cancelada</span></td><td><button class="btn-icon" onclick="editEncomenda(this)"><i class="fa-solid fa-pen"></i></button></td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Modal -->
        <div class="modal-overlay" id="encomendaModal">
            <div class="modal">
                <div class="modal-header">
                    <h2 class="modal-title">Nova Encomenda</h2>
                    <button type="button" class="close-btn" onclick="resetEncomendaModal()"><i class="fa-solid fa-xmark"></i></button>
                </div>
                <form id="formEncomenda" onsubmit="event.preventDefault(); addEncomendaRow();">
                    <div class="form-group">
                        <label>Cliente Associado</label>
                        <select class="form-control" id="eCliente" required>
                            <option value="">(Selecione um Cliente...)</option>
                            <option value="Maria João Silva">Maria João Silva</option>
                            <option value="TechStore Lda">TechStore Lda</option>
                            <option value="Rui Pereira">Rui Pereira</option>
                            <option value="Mercado Fio Unipessoal">Mercado Fio Unipessoal</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Destino</label>
                        <input type="text" class="form-control" id="eDestino" required>
                    </div>
                    <button type="submit" class="btn btn-primary" style="width:100%">Registar Encomenda</button>
                </form>
            </div>
        </div>
        <script>
            let editRowEnc = null;
            function editEncomenda(btn) {
                const tr = btn.closest('tr');
                editRowEnc = tr;
                
                // Trata de selecionar a opçao no drop down se existir
                const clName = tr.cells[1].textContent;
                const selectElement = document.getElementById('eCliente');
                let found = false;
                for(let i=0; i<selectElement.options.length; i++) {
                    if(selectElement.options[i].value === clName) {
                        selectElement.selectedIndex = i;
                        found = true;
                        break;
                    }
                }
                if(!found) selectElement.value = ""; // Default empty

                document.getElementById('eDestino').value = tr.cells[2].textContent;
                
                document.querySelector('#encomendaModal .modal-title').textContent = "Editar Encomenda";
                document.querySelector('#formEncomenda button[type="submit"]').textContent = "Atualizar Encomenda";
                openModal('encomendaModal');
            }

            function resetEncomendaModal() {
                closeModal('encomendaModal');
                document.getElementById('formEncomenda').reset();
                editRowEnc = null;
                document.querySelector('#encomendaModal .modal-title').textContent = "Nova Encomenda";
                document.querySelector('#formEncomenda button[type="submit"]').textContent = "Registar Encomenda";
            }

            function addEncomendaRow() {
                const cliente = document.getElementById('eCliente').value;
                const destino = document.getElementById('eDestino').value;
                
                if(editRowEnc) {
                    editRowEnc.cells[1].textContent = cliente;
                    editRowEnc.cells[2].textContent = destino;
                    showSimulatedToast('Encomenda atualizada!');
                } else {
                    const randId = '#' + Math.floor(10000 + Math.random() * 90000);
                    const tbody = document.querySelector('.data-table tbody');
                    if(!tbody) return;
                    const tr = document.createElement('tr');
                    tr.innerHTML = `<td>${randId}</td><td>${cliente}</td><td>${destino}</td><td>Agora mesmo</td><td><span class="status pendente">Pendente</span></td><td><button class="btn-icon" onclick="editEncomenda(this)"><i class="fa-solid fa-pen"></i></button></td>`;
                    tbody.insertBefore(tr, tbody.firstChild);
                    showSimulatedToast('Encomenda adicionada com sucesso!');
                }
                resetEncomendaModal();
            }
        </script>
    """,
    "entregas.html": """
        <div class="view-section active">
            <div class="page-header" style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h1 class="page-title">Planeamento de Entregas</h1>
                    <p class="page-subtitle">Atribuição a estafetas e rotas (Ref: 4.3)</p>
                </div>
                <button class="btn btn-primary" style="background-color: var(--success-color);" onclick="showSimulatedToast('Otimização de rotas completada com IA!')"><i class="fa-solid fa-wand-magic-sparkles"></i> Otimizar Rotas</button>
            </div>
            <div class="panels-grid">
                <div class="panel-card">
                    <h2 class="panel-title">Mapa de Zonas (Simulado)</h2>
                    <div style="background-color: #f0f0f0; height: 300px; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #888; flex-direction: column; gap: 10px;">
                        <i class="fa-solid fa-map-location-dot" style="font-size: 50px;"></i>
                        <span>Integração de Mapa Aqui</span>
                    </div>
                </div>
                <div class="panel-card">
                    <h2 class="panel-title">Enc. Pendentes</h2>
                    <div class="table-container" style="margin-top: 15px;">
                        <table class="data-table">
                            <thead><tr><th>ID</th><th>Zona</th><th>Ações</th></tr></thead>
                            <tbody>
                                <tr><td>#10024</td><td>Amadora</td><td><button class="btn btn-primary" style="padding: 4px 10px; font-size: 12px;" onclick="openAssociarModal(this, '#10024')">Associar</button></td></tr>
                                <tr><td>#10025</td><td>Sintra</td><td><button class="btn btn-primary" style="padding: 4px 10px; font-size: 12px;" onclick="openAssociarModal(this, '#10025')">Associar</button></td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!-- Associar Modal -->
        <div class="modal-overlay" id="associarModal">
            <div class="modal">
                <div class="modal-header">
                    <h2 class="modal-title">Associar a Estafeta</h2>
                    <button type="button" class="close-btn" onclick="closeModal('associarModal')"><i class="fa-solid fa-xmark"></i></button>
                </div>
                <form id="formAssociar" onsubmit="event.preventDefault(); associarEstafeta();">
                    <div class="form-group">
                        <label>Encomenda</label>
                        <input type="text" class="form-control" id="assocEnc" readonly>
                    </div>
                    <div class="form-group">
                        <label>Selecionar Estafeta Livre</label>
                        <select class="form-control" id="assocEstafeta" required>
                            <option value="Ana S.">Ana S. (Disponível)</option>
                            <option value="Carlos R.">Carlos R. (Disponível)</option>
                        </select>
                    </div>
                    <button type="submit" class="btn btn-primary" style="width:100%">Associar Definitivamente</button>
                </form>
            </div>
        </div>
        <script>
            let currentAssocBtn = null;
            function openAssociarModal(btn, encId) {
                currentAssocBtn = btn;
                document.getElementById('assocEnc').value = encId;
                openModal('associarModal');
            }
            function associarEstafeta() {
                const estafeta = document.getElementById('assocEstafeta').value;
                if(currentAssocBtn) {
                    const tr = currentAssocBtn.closest('tr');
                    tr.style.transition = 'all 0.3s';
                    tr.style.opacity = '0';
                    setTimeout(() => tr.remove(), 300);
                }
                closeModal('associarModal');
                showSimulatedToast(`Encomenda associada a ${estafeta} com sucesso!`);
                currentAssocBtn = null;
            }
        </script>
    """,
    "estafetas.html": """
        <div class="view-section active">
            <div class="page-header" style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h1 class="page-title">Gestão de Estafetas</h1>
                    <p class="page-subtitle">Disponibilidade e perfis (Ref: 4.4)</p>
                </div>
            </div>
            <div class="dashboard-grid">
                 <div class="panel-card" style="text-align: center;">
                    <img src="https://i.pravatar.cc/150?img=33" alt="" style="width: 80px; height: 80px; border-radius: 50%; margin-bottom: 10px; border: 3px solid var(--accent-color);">
                    <h3>Carlos R.</h3>
                    <p class="status distribuicao" style="display: inline-block; margin-top: 10px;">Ativo (Rota Norte)</p>
                 </div>
                 <div class="panel-card" style="text-align: center;">
                    <img src="https://i.pravatar.cc/150?img=47" alt="" style="width: 80px; height: 80px; border-radius: 50%; margin-bottom: 10px; border: 3px solid var(--success-color);">
                    <h3>Ana S.</h3>
                    <p class="status entregue" style="display: inline-block; margin-top: 10px;">Disponível</p>
                 </div>
                 <div class="panel-card" style="text-align: center;">
                    <img src="https://i.pravatar.cc/150?img=12" alt="" style="width: 80px; height: 80px; border-radius: 50%; margin-bottom: 10px; border: 3px solid var(--border-color);">
                    <h3>Miguel T.</h3>
                    <p class="status cancelada" style="display: inline-block; margin-top: 10px;">Férias</p>
                 </div>
            </div>
        </div>
    """,
    "recursos.html": """
        <div class="view-section active">
            <div class="page-header">
                <h1 class="page-title">Recursos (Veículos)</h1>
                <p class="page-subtitle">Gestão de frota (Ref: 4.5)</p>
            </div>
            <div class="panel-card">
                <div class="table-container">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Matrícula</th>
                                <th>Tipo</th>
                                <th>Estado</th>
                                <th>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr><td>AB-12-CD</td><td>Carrinha de Carga</td><td><span class="status entregue">Operacional</span></td><td><button class="btn btn-primary" style="padding: 4px 8px; font-size:12px; background:var(--warning-color); color:black; border:none;" onclick="showSimulatedToast('Alerta de Revisão enviado à oficina para o chassi AB-12-CD.')">Agendar Revisão</button></td></tr>
                            <tr><td>XY-99-ZZ</td><td>Motorizada</td><td><span class="status distribuicao">En Uso</span></td><td><button class="btn btn-primary" style="padding: 4px 8px; font-size:12px; background:var(--warning-color); color:black; border:none;" onclick="showSimulatedToast('Alerta de Revisão enviado à oficina para o chassi XY-99-ZZ.')">Agendar Revisão</button></td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    """,
    "comunicacao.html": """
        <div class="view-section active">
            <div class="page-header">
                <h1 class="page-title">Comunicação com Cliente</h1>
                <p class="page-subtitle">Notificações e Email/SMS (Ref: 4.8 - Obrigatório)</p>
            </div>
            <div class="panels-grid">
                <div class="panel-card">
                    <h2 class="panel-title">Simular Envio de Notificação</h2>
                    <div class="form-group">
                        <label>Cliente / Encomenda ID</label>
                        <input type="text" class="form-control" value="#10023 - TechStore" readonly>
                    </div>
                    <div class="form-group" style="margin-top: 15px;">
                        <label>Tipo de Mensagem</label>
                        <select class="form-control">
                            <option>Notificação de Estado (A caminho)</option>
                            <option>Aviso de Atraso</option>
                            <option>Confirmação de Entrega</option>
                        </select>
                    </div>
                    <button class="btn btn-primary" onclick="simulateClientComms()" style="margin-top: 15px;">Enviar Email / SMS</button>
                </div>
                <div class="panel-card">
                    <h2 class="panel-title">Histórico Recente</h2>
                    <div style="font-size: 13px; margin-top: 15px; border-left: 2px solid var(--border-color); padding-left: 15px;">
                        <p style="margin-bottom: 10px;"><strong>Hoje, 10:50:</strong> SMS enviado para #10023 - "A sua encomenda já se encontra em distribuição."</p>
                        <p style="margin-bottom: 10px;"><strong>Hoje, 09:15:</strong> Email enviado para #10022 - "Encomenda entregue com sucesso."</p>
                    </div>
                </div>
            </div>
        </div>
    """
}

def get_template(content, css, js):
    return f'''<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LogiTrack - Gestão Inteligente de Entregas</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        {css}
        .nav-item {{ text-decoration: none; }}
    </style>
</head>
<body>
    <div class="app-container">
        <!-- Unified Navbar -->
        <nav class="navbar">
            <div class="navbar-left">
                <a href="index.html" class="logo">
                    <i class="fa-solid fa-truck-fast"></i>
                    <span>LogiTrack</span>
                </a>
                <div class="nav-list">
                    <a href="index.html" class="nav-item">
                        <i class="fa-solid fa-chart-pie"></i>
                        <span>Dashboard</span>
                    </a>
                    <a href="clientes.html" class="nav-item">
                        <i class="fa-solid fa-users"></i>
                        <span>Clientes</span>
                    </a>
                    <a href="encomendas.html" class="nav-item">
                        <i class="fa-solid fa-box"></i>
                        <span>Encomendas</span>
                    </a>
                    <a href="entregas.html" class="nav-item">
                        <i class="fa-solid fa-route"></i>
                        <span>Entregas</span>
                    </a>
                    <a href="estafetas.html" class="nav-item">
                        <i class="fa-solid fa-motorcycle"></i>
                        <span>Estafetas</span>
                    </a>
                    <a href="recursos.html" class="nav-item">
                        <i class="fa-solid fa-truck"></i>
                        <span>Recursos</span>
                    </a>
                    <a href="comunicacao.html" class="nav-item">
                        <i class="fa-solid fa-comment-dots"></i>
                        <span>Comunicação</span>
                    </a>
                </div>
            </div>
            <div class="navbar-right">
                <div class="user-nav-profile">
                    <img src="https://i.pravatar.cc/150?img=11" alt="Admin" class="avatar" style="width: 32px; height: 32px; border: 2px solid var(--accent-color);">
                    <button class="logout-btn" onclick="logout()">
                        <i class="fa-solid fa-right-from-bracket"></i>
                        Sair
                    </button>
                </div>
            </div>
        </nav>

        <!-- Main Content -->
        <main class="main-content">

            <!-- Dynamic Views (Integrated directly) -->
            <div class="views-container" id="views-container">
                {content}
            </div>
        </main>
    </div>

    <!-- Toast Notifications Container -->
    <div id="toast-container" class="toast-container"></div>

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        {js}
    </script>
</body>
</html>'''

for filename, content in pages.items():
    filepath = os.path.join(base_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(get_template(content, css_content, js_content))

print("All HTML pages generated successfully with INLINE JS/CSS.")
