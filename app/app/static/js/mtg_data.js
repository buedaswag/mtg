
var card_name_list = '{{ card_name_list }}'
var toAdd = document.createDocumentFragment();
for(var i=0; i < card_name_list.length; i++){
   var new_li = document.createElement('LI');
   new_li.id = 'r'+i;
   new_li.className = 'ansbox';
   toAdd.appendChild(new_li);
}

var variable1 = "someString";
$('#demo').load(
    "{{ url_for('addshare2', share='ADDSHARE2') }}".replace("ADDSHARE2", variable1)
);

document.getElementById('side-menu').appendChild(toAdd);