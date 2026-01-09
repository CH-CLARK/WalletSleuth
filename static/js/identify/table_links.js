$(document).ready(function () {
    const currencyMap = {
        BTC: 'bitcoin',
        BCH: 'bitcoin-cash',
        BSV: 'bitcoin-cash',
        LTC: 'litecoin',
        ETH: 'ethereum',
        DOGE: 'dogecoin',
        ADA: 'cardano',

    };

    var table = $('#outputTable').DataTable({
        colResize: { realtime: true },
        ajax: {
            url: '/get_csv_data',
            type: 'POST',
            dataSrc: 'data'
        },
        columns: [
            { data: 'Type', width: '10%' },
            { data: 'Currency', width: '8%' },

            { 
                data: 'Address/Transaction',
                width: '30%',
                render: function (data, type, row) {
                    if (type === 'display') {
                        return `
                            <div class="address-cell" style="position:relative;">
                                <span class="action-wrapper">
                                    <span class="action-icon" style="cursor:pointer;">🧭</span>
                                    <div class="action-menu" style="display:none; background:#fff; border:1px solid #ccc; padding:4px; z-index:9999; box-shadow:0 2px 6px rgba(0,0,0,0.15);"></div>
                                </span>
                                ${data}
                            </div>
                        `;
                    }
                    return data;
                }
            },
            
            { data: 'Wallet', width: '15%' },
            { data: 'Path', width: '50%' }
        ],
        scrollY: '32rem',
        scrollX: true,
        scrollCollapse: true,
        paging: false,
        autoWidth: false,
        fixedHeader: true,
        deferRender: true
    });

    table.on('draw', function () {
        $('#outputTable tbody tr').each(function () {
            const row = $(this);
            const rowData = table.row(row).data();
            if (!rowData) return;

            const fullCurrency = rowData.Currency;
            const typeCol = rowData['Type']
            const address = rowData['Address/Transaction'];
            const menu = row.find('.action-menu');
            menu.empty();

            const codeMatch = fullCurrency.match(/\(([^)]+)\)/);
            const currencyCode = codeMatch ? codeMatch[1].toUpperCase() : null;

            if (typeCol.startsWith('Add')) {
                if (currencyMap[currencyCode]) {
                    menu.append(`<div class="blockchair-action" style="cursor:pointer;">
                        <img src="/static/app_files/third_party_icons/blockchair.cube.png" style="width:16px;height:16px;margin-right:6px;">View on Blockchair
                        </div>`);

                }
                
                if (address.startsWith('0x')) {
                    menu.append(`<div class="etherscan-action" style="cursor:pointer;">
                        <img src="/static/app_files/third_party_icons/etherscan-logo-circle.svg" style="width:16px;height:16px;margin-right:6px;">View on Etherscan
                        </div>`);
                }

                if (!currencyMap[currencyCode] && !address.startsWith('0x') ) {
                    menu.append(`<div>❌ Currency not yet supported!</div>`);
                }
            }
            
            if (typeCol.startsWith('Trans')){
                menu.append(`<div>❌ Transactions are not yet supported!</div>`);
            }
            

            if (typeCol.startsWith('Extended')){
                menu.append(`<div>❌ Extended Public Keys are not yet supported!</div>`);
            }

        });
    });

    $('#outputTable tbody').on('click', '.action-icon', function (e) {
        e.stopPropagation();
        $('.action-menu').hide();

        const menu = $(this).siblings('.action-menu');
        const offset = $(this).offset();
        const height = $(this).outerHeight();

        menu.css({
            position: 'fixed',
            top: offset.top + height + 2,
            left: offset.left,
            display: 'block'
        });
    });

    //Blockchair click
    $('#outputTable tbody').on('click', '.blockchair-action', function (e) {
        e.stopPropagation();
        const rowData = table.row($(this).closest('tr')).data();
        const fullCurrency = rowData.Currency;
        const address = rowData['Address/Transaction'];
        const codeMatch = fullCurrency.match(/\(([^)]+)\)/);
        const currencyCode = codeMatch ? codeMatch[1].toUpperCase() : null;
        const chain = currencyMap[currencyCode];
        if (!chain) return;
        window.open(`https://blockchair.com/${chain}/address/${encodeURIComponent(address)}`, '_blank');
    });

    //Etherscan click
    $('#outputTable tbody').on('click', '.etherscan-action', function (e) {
        e.stopPropagation();
        const rowData = table.row($(this).closest('tr')).data();
        const address = rowData['Address/Transaction'];
        window.open(`https://www.etherscan.io/address/${encodeURIComponent(address)}`, '_blank');
    });

    $(document).on('click', function () {
        $('.action-menu').hide();
    });

});