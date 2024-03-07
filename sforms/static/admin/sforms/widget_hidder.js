window.addEventListener('load', function(e) {

    var MULTITYPES = ['multicheckbox', 'radio', 'choice'];

    function toogle_textarea(_item) {
        var item = _item.target ? _item.target : _item;
        var id = item.id;
        if (id && id.indexOf('__prefix__') == -1){
            var tx = document.getElementById(id.replace('-fieldtype', '-values'));
            var _tx = tx.parentNode;
            while (_tx) {
                if (_tx && _tx.className && _tx.className.indexOf('form-row') !== -1) {
                    tx = _tx;
                    break;
                }
                _tx = _tx.parentNode;
            }
            var selectedElement = item.options[item.selectedIndex];
            if (selectedElement.value && MULTITYPES.indexOf(selectedElement.value) != -1) {
                tx.style.display = 'block';
            } else {
                tx.style.display = 'none';
            }
        }
    }

    document.querySelectorAll('select[name*="-fieldtype"]').forEach(function(node){
        toogle_textarea(node);
        node.addEventListener('change', toogle_textarea)
    });


});