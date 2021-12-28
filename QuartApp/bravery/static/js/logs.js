$(function(){

    // refresh automatiquement toutes les secondes
    window.setInterval(function(){
        loadNewLogs();

    }, 1000)

    function loadNewLogs(){
        var log_container = document.getElementById("log_container");
        $.ajax({
            url: "/bravery/update_logs",
            type: "POST",
            dataType: "json",
            success: function(data){

                // On conserve le scroll pour être au même endroit quand la page va reload 
                var oldscroll = document.getElementById('logs').scrollTop;

                // ici data est le contenu de logs_model modifié
                log_container.innerHTML = data;
                filterLogs();
                document.getElementById('logs').scrollTop = oldscroll;
            }
        });
    }

});

// Filtre champions
function filterLogs() {
	var input = document.getElementById('logFilter');
	var filter = input.value.toLowerCase();

	var logs = document.getElementsByClassName("log_container");
	for (var log of logs) {
		logIp = log.children[1].innerText ;
		if (logIp.includes(filter) || filter == ""){
			log.style.display = "block";
		}
		else{
			log.style.display = "none";
		}
	}
}

function resetLogs(){
	$.post('/bravery/reset_log');
}