if(confirm("Aimez-vous le cinéma?"))
	alert('Bienvenue sur le site');
else{
	alert("accès refusé!")
    document.location.href="http://www.google.fr"; 
    }

    var bienvenue = document.getElementById('bienvenue');

  
   
   bienvenue.addEventListener('click', function(e) {

       e.target.innerHTML = '! eunevneiB';

   });