function switchVisible() {
            if (document.getElementById('login-button')) {
                document.getElementById('login-button').style.display = 'none';
                document.getElementById('container').style.display = 'block';
            }
}

function switchInvisible() {
            if (document.getElementById('container')) {
                document.getElementById('container').style.display = 'none';
                document.getElementById('login-button').style.display = 'block';
            }
}

function show_log() {
			if (document.getElementById('container')) {
                document.getElementById('container').style.display = 'none';
                document.getElementById('show_log').style.display = 'block';
            }
}

function show_befor() {
			if (document.getElementById('show_log')) {
                document.getElementById('show_log').style.display = 'none';
                document.getElementById('container').style.display = 'block';
            }
}










