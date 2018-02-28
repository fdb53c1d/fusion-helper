(function() {
    'use strict';

    //Sorts table rows by specified column
    //Doesn't do natural sort on alphanumeric strings
    function sortTable(table, col, reverse) {
        var tbody = table.tBodies[0],
            trows = Array.prototype.slice.call(tbody.rows);
        reverse = -((+reverse) || -1);

        trows.sort(function (_a, _b) {
            var a = _a.cells[col].textContent,
                b = _b.cells[col].textContent,
                aId = _a.cells[0].textContent,
                bId = _b.cells[0].textContent;

            if (a === b) return (aId - bId); //If equal, sort by the Id

            //return reverse * a.localeCompare(b, undefined, {numeric: true}); (Too slow!)

            if(isNaN(parseInt(a)) || isNaN(parseInt(b))) {
                return reverse * (a < b ? -1 : (a > b ? 1 : 0));
            }
            return reverse * (a - b);
        });

        trows.forEach(function (e) {
            tbody.appendChild(e);
        });
    }

    function clearState(table) {
        var cells = Array.prototype.slice.call(table.tHead.rows[0].cells);

        cells.forEach(function (e) {
            var sortState = e.querySelector('.sort-state');
            sortState.dataset.state = 'none';
            sortState.innerHTML = '\u2014';
        });
    }

    function updateState(table, col) {
        if (this.dataset.state === 'none') {
            clearState(table);
            sortTable(table, col, false);
            this.dataset.state = 'asc';
            this.innerHTML = '\u25B2';
        }
        else if (this.dataset.state === 'asc') {
            clearState(table);
            sortTable(table, col, true);
            this.dataset.state = 'desc';
            this.innerHTML = '\u25BC';
        }
        else if (this.dataset.state === 'desc') {
            clearState(table);
            sortTable(table, 0, false);
            this.dataset.state = 'none';
            this.innerHTML = '\u2014';
        }
    }

    function makeSortable(table) {
        var cells = Array.prototype.slice.call(table.tHead.rows[0].cells);

        cells.forEach(function (e, i) {
            var sortState = document.createElement('span');
            sortState.className = 'sort-state';
            sortState.dataset.state = 'none';
            sortState.innerHTML = '\u2014';
            sortState.style.cursor = 'pointer';
            sortState.style.padding = '5px';

            e.appendChild(sortState);
            sortState.addEventListener('click', function () {
                updateState.bind(this)(table, i);
            });
        });
    }

    window.onload = function () {
        makeSortable(document.getElementById('card-table'));
    };

})();
