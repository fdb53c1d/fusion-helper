(function() {
    'use strict';

    function getFusions(id_list, callback) {
        let request = new XMLHttpRequest(),
            url = static_root + 'api/fusions/' + id_list.join('-');

        request.onreadystatechange = function() {
            if(request.readyState === 4 && request.status === 200) {
                let fusions = JSON.parse(request.responseText);
                callback(fusions);
            }
        };
        request.open('GET', url, true);
        request.send();
    }

    function displayFusions(fusions) {
        let results = new Set(fusions.map(fusion => fusion.Result)),
            display = {},
            results_div = document.getElementById('results');
        results_div.innerHTML = '';
        results.forEach(function(result) {
            display[result] = fusions.filter(fusion => fusion.Result === result)
                .map(function(fusion) {
                let arr = [];
                for(let key in fusion)
                    if(~key.indexOf('Card'))
                        arr.push(fusion[key]);
                return arr;
            }).sort((a,b) => (a.length - b.length));
        });
        Object.keys(display).forEach(function(key) {
            results_div.innerHTML += '\n' + card_list[key].Name + '\n';
            display[key].forEach(function(x) {
                let out = '   ';
                x.forEach((y,i) => (out += card_list[y].Name + (x[i+1] ? ' + ' : '')));
                results_div.innerHTML += out + '\n';
            });
        });
    }

    function onSelect(term, card_list, idx) {
        let id_inputs = document.getElementsByClassName('cardid'),
            id_input = document.querySelector('input[name="cardid' + (idx+1) + '"]'),
            card_preview = document.getElementById('cardpreview' + (idx+1)),
            id_list = [];

        Object.keys(card_list).forEach(function(key) {
            if(card_list[key].Name === term) {
                id_input.value = key;
                card_preview.innerHTML = '';
                var cardinfo = document.createElement('span');
                cardinfo.innerHTML = '<b>Atk:</b> ' + card_list[key].Attack + '<br><br>';
                cardinfo.innerHTML += '<b>Def:</b> ' + card_list[key].Defense + '<br><br>';
                cardinfo.innerHTML += '<b>Type:</b> ' + card_types[card_list[key].Type];
                card_preview.appendChild(cardinfo);
                /*var img = document.createElement('IMG');
                img.src = static_root + 'img/cards/' + key + '.png';
                card_preview.appendChild(img);*/
            }
        });

        for(let i = 0; i < id_inputs.length; i++) {
            if(id_inputs[i].value && !isNaN(parseInt(id_inputs[i].value)))
                id_list.push(parseInt(id_inputs[i].value));
        }
        if(id_list.length < 2) return;

        getFusions(id_list, displayFusions);
    }

    function makeCompletable(inputs, card_list) {
        let completables = [],
            name_list = Object.keys(card_list).map(key => card_list[key].Name);

        for(let i = 0; i < inputs.length; i++) {
            completables.push(new autoComplete({
                selector: 'input[name="cardinput' + (i+1) + '"]',
                minChars: 2,
                cache: false,
                source: function(term, suggest) {
                    term = term.toLowerCase();
                    var matches = name_list.filter(name => ~name.toLowerCase().indexOf(term));
                    suggest(matches);
                },
                onSelect: function(event, term, item) {
                    onSelect(term, card_list, i);
                }
            }));
        }
        return completables;
    }

    window.onload = function() {
        var inputs = document.getElementsByClassName('cardinput');
        var completables = makeCompletable(inputs, card_list);
    }

})();