/*  
    Creata da Luigi Cama[Tube] 
    13 Aprile 2024
    Seguimi su https://www.youtube.com/@camatubeofficial
*/

var app = angular.module('CamApp', ['ui.bootstrap']);

// Soluzione al conflitto tra Flask/Jinja e AngularJS riguardo le doppie graffe
app.config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('{a');
    $interpolateProvider.endSymbol('a}');
}]);


app.controller('MainController', function($scope, $http, $interval, $filter) {

  $('#loader').hide();
  $('#menu').hide();
  $('#ytvideo').hide();
  $('#ytchat').hide();
  document.getElementById("zoom-controls-v").style.display = 'none';

  /*  
    Gestione errori 
      0 - formato idlive errato
      1 - video live non trovato, oppure, non è una live ma un video normale, oppure, la chat non è più disponibile in quella live
      2 - problema di connessione sconosciuto
      3 - connessione chat avviata
  */

  $scope.chatlive = [];
  $scope.chatlivefiltered = [];
  idlive_ripulito = '';

  $scope.verifica_chat = function(idlive) {
    
      $http({
          method: 'GET',
          url: '/verifica_chat',
          params: { idlive: idlive }
        }).then(function(response) {

          if (response.data.response!=0 && response.data.response!=1 && response.data.response!=2){
            $scope.avvia_chat(response.data.response);
            idlive_ripulito = response.data.response;
            $('#avvio').hide();
            $('#loader').show();
          }

          if (response.data.response==2){
            $scope.openAlert('Il video non è disponibile oppure la chat non è pubblica. Ritenta! Chissà che non accada un miracolo :)');
          }

          if (response.data.response==1){
            $scope.openAlert('URL video errato! Accetta il formato https://www.youtube.com/watch?v=Adht6WnbdR8 oppure https://youtu.be/v=Adht6WnbdR8');
          }

          if (response.data.response==0){
            $scope.openAlert('Non hai incollato l\'URL del video! Accetta il formato https://www.youtube.com/watch?v=Adht6WnbdR8 oppure https://youtu.be/v=Adht6WnbdR8');
          }

        }).catch(function(error) {
          console.error('Error fetching data:', error);
        });
      };

  $scope.avvia_chat = function(idlive){

    // Preleviamo i messaggi dal db locale
    avvia_aggiornamento(idlive);

    //Apriamo il video
    onYouTubeIframeAPIReady(idlive);

    // Imposta dinamicamente src dell'iframe
    var div = document.getElementById('ytchat');
    var iframe = div.getElementsByTagName('iframe')[0]; // Otteniamo il primo iframe all'interno del div
    if (iframe) {
      iframe.src = 'https://www.youtube.com/live_chat?v='+idlive+'&embed_domain=localhost&dark_theme=1';   
    }

    $http({
      method: 'GET',
      url: '/connessione_chat',
      params: { idlive: idlive }
    }).then(function() {

    })
    .catch(function(error) {
        console.error('Error fetching data:', error);
    });
  }     

  function aggiorna_messaggi(idlive){
    $http({
      method: 'GET',
      url: '/aggiorna_messaggi',
      params: { idlive: idlive }
    }).then(function(response) {            
        if (response) {
            $('#loader').hide();
            $('#menu').show(); 
            $('#ytvideo').show();
            $('#ytchat').show();
            $scope.chatlive = response.data;
            $chatlivefiltered = response.data;
            $scope.updateSorting(); // Verifica ordinamento dei messaggi per data e da qui richiama filtro per autore, se selezionato
            updateUsers();
          }   
    })
    .catch(function(error) {
        console.error('Error fetching data:', error);
    }); 
  }     
  

  function avvia_aggiornamento(idlive){
    $interval(function() {
      aggiorna_messaggi(idlive);
    }, 5000);
  }
 

  $scope.openAlert = function(msg) {
    $scope.message = msg;
    var myModal = new bootstrap.Modal(document.getElementById('alertModal'), {
      keyboard: true, // L'utente può chiudere il modal premendo il tasto 'Esc'
      //backdrop: 'static', // Il modal non si chiude cliccando sullo sfondo
      focus: true // Il focus viene posto automaticamente sul modal appena viene aperto
    });
    myModal.show();
  };

  $scope.openModalUser = function() {
    var myModal = new bootstrap.Modal(document.getElementById('userModal'), {
      keyboard: true, 
      //backdrop: 'static', 
      focus: true 
    });
    myModal.show();
  };

  $scope.closeModalUser = function() {
    $('#userModal').modal('hide'); // Chiude la modal
  };

  $scope.users = [];

  // Funzione per aggiornare gli utenti in base ai messaggi
  function updateUsers() {

    // Estrai gli autori univoci da $scope.chatlive e li inserisci in $scope.users in ordine alfabetico
    $scope.chatlive.forEach(function(message) {
      // Verifica se l'autore è già presente in $scope.users
      var existingUser = $scope.users.find(function(user) {
        return user.name === message.autore;
      });

      // Se l'autore non è ancora stato aggiunto, lo aggiungi a $scope.users
      if (!existingUser) {
        $scope.users.push({ name: message.autore });
      }
    });

    // Ordina $scope.users in base al nome dell'autore
    $scope.users.sort(function(a, b) {
      return a.name.localeCompare(b.name);
    });
  }

  // Funzione per aggiornare i messaggi visualizzati in base agli autori selezionati
  $scope.updateMessages = function() {
    // Usa il filtro 'selectedUsers' per filtrare i messaggi in base agli autori selezionati
    $scope.chatlivefiltered = $filter('selectedUsers')($scope.chatlive, $scope.selectedUsers);
  };

  // Funzione per confermare la selezione degli utenti
  $scope.toggleUserSelection = function() {
    var selectedUsers = $scope.users.filter(function(user) {
      return user.selected;
    });
    $scope.selectedUsers = selectedUsers.map(function(user) {
      return user.name;
    });
    // Aggiorna i messaggi filtrati
    $scope.updateMessages();
  };

  // Inizializza la variabile per mostrare/nascondere
  $scope.isDateVisible = false;
  $scope.isVideoVisible = true;
  $scope.isYTChatVisible = true;

  // Inizializza lo zoom
  $scope.zoom_chat = 150;  

  $scope.divStyle = {
    top: '10px',
    left: '800px',
    width: '560px',
    height: '315px',
    transform: 'scale(1)'
  };

  var isDragging = false;
  var startX, startY;
  var currentScale = 1;
  var isToggleDrag = false;

  $scope.zoomInDiv = function() {
    currentScale += 0.1;
    $scope.divStyle.transform = 'scale(' + currentScale + ')';
  };

  $scope.zoomOutDiv = function() {
    currentScale -= 0.1;
    $scope.divStyle.transform = 'scale(' + currentScale + ')';
  };

  $scope.startDrag = function(event) {
    if (isToggleDrag) {
      isDragging = true;
      startX = event.clientX - parseInt($scope.divStyle.left);
      startY = event.clientY - parseInt($scope.divStyle.top);
    }

    // Aggiungi l'evento mouseup al documento
    document.addEventListener('mouseup', $scope.endDrag);

  };

  $scope.endDrag = function() {
    isDragging = false;
    // Rimuovi l'evento mouseup dal documento
    document.removeEventListener('mouseup', $scope.endDrag);
  };

  document.addEventListener('mousemove', function(event) {
    if (isDragging) {
      // Calcoliamo le nuove coordinate del div
      var newLeft = event.clientX - startX;
      var newTop = event.clientY - startY;
  
      // Limitiamo lo spostamento del div all'interno della finestra del browser
      var windowWidth = window.innerWidth;
      var windowHeight = window.innerHeight;
      var divWidth = parseInt($scope.divStyle.width);
      var divHeight = parseInt($scope.divStyle.height);
  
      // Impostiamo i limiti del div all'interno della finestra del browser
      var maxX = windowWidth - divWidth;
      var maxY = windowHeight - divHeight;
  
      // Assicuriamoci che il div non superi i limiti della finestra
      newLeft = Math.max(0, Math.min(newLeft, maxX));
      newTop = Math.max(0, Math.min(newTop, maxY));
  
      // Aggiorniamo le coordinate del div
      $scope.divStyle.left = newLeft + 'px';
      $scope.divStyle.top = newTop + 'px';
  
      $scope.$apply();
    }
  });

  $scope.toggleDrag = function() {
    isToggleDrag = !isToggleDrag;
  };

  // Funzione per aumentare lo zoom
  $scope.zoomIn = function(div) {
    $scope[div] += 10; // Aumenta lo zoom di 10%
  };

  // Funzione per diminuire lo zoom
  $scope.zoomOut = function(div) {
    $scope[div]  -= 10; // Diminuisce lo zoom di 10%
  };

  // Funzione per mostrare o nascondere la data
  $scope.toggleDate = function() {
      $scope.isDateVisible = !$scope.isDateVisible;
  };

  // Funzione per mostrare o nascondere il video
  $scope.toggleVideo = function() {
    $scope.isVideoVisible = !$scope.isVideoVisible;
  };

  // Funzione per mostrare o nascondere la chat di Youtube
  $scope.toggleYTChat = function() {
    $scope.isYTChatVisible = !$scope.isYTChatVisible;
    if ($scope.isYTChatVisible==true){
      var div = document.getElementById('ytchat');
      var iframe = div.getElementsByTagName('iframe')[0]; // Otteniamo il primo iframe all'interno del div
      if (iframe) {
        iframe.src = 'https://www.youtube.com/live_chat?v='+idlive_ripulito+'&embed_domain=localhost&dark_theme=1';   
      }
    }
  };

  $scope.showControls = function(div) {
    document.getElementById("zoom-controls-"+div).style.display = "block";
  };

  $scope.hideControls = function(div) {
    document.getElementById("zoom-controls-"+div).style.display = "none";
  };

  // Funzione per ordinare gli oggetti in base all'ordine selezionato
  $scope.updateSorting = function() {
    if ($scope.orderType === 'dateAsc') {
        $scope.chatlivefiltered = $scope.chatlive.sort(function(a, b) {
            return new Date(a.data) - new Date(b.data);
        });
    } else if ($scope.orderType === 'dateDesc') {
        $scope.chatlivefiltered = $scope.chatlive.sort(function(a, b) {
            return new Date(b.data) - new Date(a.data);
        });
    }
    $scope.updateMessages();
  };


  // Inizializza l'ordinamento con l'ordinamento crescente di default
  $scope.orderType = 'dateDesc';
  $scope.updateSorting();

  // Aggiorna l'ordinamento quando l'utente cambia la selezione
  $scope.$watch('orderType', function(newValue, oldValue) {
      if (newValue !== oldValue) {
          $scope.updateSorting();
      }
  });

  // YouTube Player
  function onYouTubeIframeAPIReady(idlive) {
    // Crea un nuovo player video
    var player = new YT.Player('player', {
        height: '315',
        width: '560',
        videoId: idlive,
        playerVars: {
            'autoplay': 1, // Riproduzione automatica
            'controls': 1, // Mostra i controlli del video
            'rel': 0, // Non mostrare video correlati alla fine
            'showinfo': 0 // Nascondi informazioni sul video
        }
    });
}

$scope.openNewWindow = function(url) {
  window.open('https://www.youtube.com/channel/'+url, '_blank');
};

});

app.filter('selectedUsers', function() {
  return function(messages, selectedUsers) {
    if (!selectedUsers || selectedUsers.length === 0) {
      return messages;
    }

    // Filtra i messaggi in base agli autori selezionati
    return messages.filter(function(message) {
      return selectedUsers.includes(message.autore);
    });
  };
});

       


