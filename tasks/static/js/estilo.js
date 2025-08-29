let datatable;
let modalRelaciones; 

const pedrito = {
    orderCellsTop: true,
    columns: Array(7).fill({ className: 'centered' }),
    language: {
        lengthMenu: '_MENU_',
        info: "Mostrando _START_ a _END_ de _TOTAL_ entradas",
        infoEmpty: "No hay datos disponibles",
        infoFiltered: "(filtrado de _MAX_ entradas totales)",
        zeroRecords: "No se encontraron coincidencias",
        search: "Buscar:",
        paginate: {
            first: '<i class="bi bi-chevron-double-left"></i>',
            last: '<i class="bi bi-chevron-double-right"></i>',
            next: '<i class="bi bi-chevron-right"></i>',
            previous: '<i class="bi bi-chevron-left"></i>'
        }
    },
    initComplete: function () {
        const api = this.api();
        const headerRow = $(api.table().header()).find('tr').eq(1);

        api.columns().every(function (index) {
            const column = this;
            const headerCell = headerRow.find('th').eq(index).get(0);

            if ([2, 3].includes(index)) {
                const select = document.createElement('select');
                select.classList.add('form-select', 'form-select-sm');
                select.add(new Option(''));
                headerCell.innerHTML = '';
                headerCell.appendChild(select);

                select.addEventListener('change', function () {
                    column.search(this.value).draw();
                });

                column.data().unique().sort().each(function (d) {
                    if (d?.trim()) {
                        select.add(new Option(d));
                    }
                });

            } else if ([1, 4].includes(index)) {
                const input = document.createElement('input');
                input.type = 'text';
                input.classList.add('form-control', 'form-control-sm');
                input.placeholder = $(headerCell).text() || 'Buscar...';

                headerCell.innerHTML = '';
                headerCell.appendChild(input);

                input.addEventListener('keyup', function () {
                    if (column.search() !== this.value) {
                        column.search(this.value).draw();
                    }
                });
            }
        });
    }
};

const listaObjeto = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/lista_objeto');
        const data = await response.json();

        let rows = '';

        data.data.forEach((objeto, index) => {
            rows += `
                <tr>
                    <td>${index + 1}</td>
                    <td>${objeto.nombre}</td>
                    <td>${objeto.t_objeto}</td>
                    <td>${objeto.estatus}</td>
                    <td>${objeto.descripcion}</td>
                    <td>
                        <button class="btn btn-primary btn-sm" onclick="mostrarRelaciones(${objeto.id})">
                            Relaciones
                        </button>
                    </td>
                    <td>
                        <a href="/actualizar/${objeto.id}/" class="btn btn-warning btn-sm" aria-label="Editar ingresos">
                            <i class="bi bi-pencil"></i>
                        </a>
                    </td>
                </tr>
            `;
        });

        document.querySelector('#datatable tbody').innerHTML = rows;
    } catch (error) {
        alert("Error al cargar datos: " + error);
    }
};

const intDataTable = async () => {
    if ($.fn.DataTable.isDataTable('#datatable')) {
        $('#datatable').DataTable().clear().destroy();
    }

    await listaObjeto();

    datatable = $('#datatable').DataTable(pedrito);
};

async function mostrarRelaciones(id) {
    const modalElement = document.getElementById('relacionesModal');
    if (!modalElement) {
        alert('No se encontró el modal relacionesModal en el DOM');
        return;
    }

    if (!modalRelaciones) {
        modalRelaciones = new bootstrap.Modal(modalElement, {
            backdrop: 'static',
            keyboard: false
        });
    }

    const contenido = document.getElementById('contenidoRelaciones');
    contenido.innerHTML = 'Cargando...';

    modalRelaciones.show();

    try {
        const response = await fetch(`http://127.0.0.1:8000/relaciones_objeto/${id}`);
        const data = await response.json();

        let html = '<strong>Base en:</strong><br>';
        html += data.llama.length
            ? '<ul>' + data.llama.map(o => `<li>${o.nombre} (${o.t_objeto}) - ${o.estatus}</li>`).join('') + '</ul>'
            : '<p>No llama a ningún objeto.</p>';

        html += '<strong>Referencia en:</strong><br>';
        html += data.llamado_por.length
            ? '<ul>' + data.llamado_por.map(o => `<li>${o.nombre} (${o.t_objeto}) - ${o.estatus}</li>`).join('') + '</ul>'
            : '<p>No es llamado por ningún objeto.</p>';

        contenido.innerHTML = html;
    } catch (error) {
        contenido.innerHTML = `<div class="alert alert-danger" role="alert">
            Error al obtener relaciones: ${error}
        </div>`;
    }
}

window.addEventListener('load', intDataTable);
