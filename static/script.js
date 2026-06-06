// Array para almacenar los textos
let textos = [];

// Elementos del DOM
const razaSelect = document.getElementById('raza');
const ambienteSelect = document.getElementById('ambiente');
const extensionSelect = document.getElementById('extension');
const vistaPreviaDiv = document.getElementById('vistaPrevia');

// Función para generar el texto basado en los selectores
function generarTexto() {
    const raza = razaSelect.value;
    const ambiente = ambienteSelect.value;
    const extension = extensionSelect.value;
    
    // Formato: "Estas en un {extension,ambiente}, donde viven los {raza}"
    return `Estas en un ${extension} de ${ambiente}, donde viven los ${raza}`;
}

// Función para actualizar la vista previa
function actualizarVistaPrevia() {
    const textoGenerado = generarTexto();
    vistaPreviaDiv.textContent = textoGenerado;
}

// Agregar event listeners para actualizar la vista previa
if (razaSelect) {
    razaSelect.addEventListener('change', actualizarVistaPrevia);
}
if (ambienteSelect) {
    ambienteSelect.addEventListener('change', actualizarVistaPrevia);
}
if (extensionSelect) {
    extensionSelect.addEventListener('change', actualizarVistaPrevia);
}

// Cargar datos del servidor al iniciar
async function cargarDatosIniciales() {
    try {
        const response = await fetch('/api/textos');
        if (!response.ok) {
            throw new Error('No se pudo cargar los datos del servidor');
        }
        const data = await response.json();
        textos = data.textos || [];
        renderizarLista();
        console.log('Datos cargados del servidor:', textos);
    } catch (error) {
        console.error('Error al cargar datos:', error);
        mostrarError('Error al cargar los textos. Por favor, recarga la página.');
    }
}

// Mostrar mensaje de error
function mostrarError(mensaje) {
    const contenedor = document.getElementById('listaTextos');
    contenedor.innerHTML = `<div class="texto-item" style="text-align: center; color: #dc3545;">❌ ${mensaje}</div>`;
}

// Renderizar la lista de textos
function renderizarLista() {
    const contenedor = document.getElementById('listaTextos');
    
    if (textos.length === 0) {
        contenedor.innerHTML = '<div class="texto-item" style="text-align: center; color: #666;">📝 No hay textos aún. ¡Crea el primero usando el botón + Crear Texto!</div>';
        return;
    }
    
    contenedor.innerHTML = textos.map(texto => `
        <div class="texto-item" data-id="${texto.id}">
            <div class="texto-contenido">${escapeHtml(texto.texto)}</div>
            <div class="texto-fecha">📅 ${texto.fecha}</div>
            <button class="btn-eliminar" onclick="eliminarTexto(${texto.id})">🗑️ Eliminar</button>
        </div>
    `).join('');
}

// Función para escapar HTML (seguridad)
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Función para agregar nuevo texto (usando los selectores)
async function agregarTexto() {
    const textoGenerado = generarTexto();
    
    const nuevoItem = {
        id: Date.now(),
        texto: textoGenerado
    };
    
    try {
        const response = await fetch('/api/textos', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(nuevoItem)
        });
        
        if (!response.ok) {
            throw new Error('Error al guardar el texto');
        }
        
        const result = await response.json();
        if (result.success) {
            await cargarDatosIniciales(); // Recargar la lista
            return true;
        } else {
            throw new Error(result.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('❌ Error al guardar el texto. Por favor, intenta de nuevo.');
        return false;
    }
}

// Función para eliminar texto
async function eliminarTexto(id) {
    if (confirm('¿Estás seguro de que quieres eliminar este texto?')) {
        try {
            const response = await fetch(`/api/textos/${id}`, {
                method: 'DELETE'
            });
            
            if (!response.ok) {
                throw new Error('Error al eliminar el texto');
            }
            
            const result = await response.json();
            if (result.success) {
                await cargarDatosIniciales(); // Recargar la lista
            } else {
                throw new Error(result.error);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('❌ Error al eliminar el texto. Por favor, intenta de nuevo.');
        }
    }
}

// Modal functionality
const modal = document.getElementById('modalAgregar');
const btnAgregar = document.getElementById('btnAgregar');
const btnGuardar = document.getElementById('btnGuardar');
const btnCancelar = document.getElementById('btnCancelar');
const closeBtn = document.querySelector('.close');

// Abrir modal y resetear selectores
btnAgregar.onclick = function() {
    // Resetear selectores a valores por defecto
    razaSelect.value = 'humanos';
    ambienteSelect.value = 'bosques';
    extensionSelect.value = 'pueblo';
    
    // Actualizar vista previa
    actualizarVistaPrevia();
    
    modal.style.display = 'block';
}

// Cerrar modal
function cerrarModal() {
    modal.style.display = 'none';
}

closeBtn.onclick = cerrarModal;
btnCancelar.onclick = cerrarModal;

// Guardar texto
btnGuardar.onclick = async function() {
    const exito = await agregarTexto();
    if (exito) {
        cerrarModal();
    }
}

// Cerrar modal haciendo clic fuera
window.onclick = function(event) {
    if (event.target == modal) {
        cerrarModal();
    }
}

// Inicializar la aplicación
cargarDatosIniciales();