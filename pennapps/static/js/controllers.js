'use strict';

/* Controllers */



var phonecatControllers = angular.module('phonecatControllers', []);

var phonecatControllers = angular.module('phonecatControllers', [])
    .config(['$httpProvider', function($httpProvider) {
        $httpProvider.defaults.timeout = 50000;
}]);

phonecatControllers.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

var globalCounter = 0;

phonecatControllers.controller('PhoneListCtrl', ['$scope', 'Phone',
  function($scope, Phone) {
    $scope.phones = Phone.query();
    $
    $scope.orderProp = '-likes';
  }]);


phonecatControllers.controller('PhoneDetailCtrl', ['$scope', '$routeParams', 'Phone',
  function($scope, $routeParams, Phone) {
    $scope.phone = Phone.get({phoneId: $routeParams.phoneId}, function(phone) {
      $scope.mainImageUrl = phone.images[0];
    });

    $scope.setImage = function(imageUrl) {
      $scope.mainImageUrl = imageUrl;
    }
  }]);

angular.module('genre', []);

function GenreCtrl($scope) {
    $scope.genre = [
        {'name': 'Reggae', 'genre': 'Reggae'},
        {'name': 'Classical', 'genre': 'classical'}




        ];
    
    $scope.genreIncludes = ["Reggae","Classical","Pop","Electronic","Rock/Metal","Alternative","Country/Folk","ClassicRock","Jazz","Hip-Hop","Rap","Other"];
    
    $scope.includeGenre = function(genre) {
        var i = $.inArray(genre, $scope.genreIncludes);
        if (i > -1) {
            $scope.genreIncludes.splice(i, 1);
        } else {
            $scope.genreIncludes.push(genre);
        }
    }

   
$scope.input = "";
$scope.clearInput = function() {
  $scope.input = "";
};
    


    $scope.genreIsReggae = function(genre) {
        if (genre == 'Reggae') {
            return true;
        }
        return false;
    }

    $scope.genreIsElectronic = function(genre) {
        if (genre == 'Electronic') {
            return true;
        }
        return false;
    }


    $scope.genreIsPop = function(genre) {
        if (genre == 'Pop') {
            return true;
        }
        return false;
    }

    $scope.genreIsRockMetal = function(genre) {
        if (genre == 'Rock/Metal') {
            return true;
        }
        return false;
    }

    $scope.genreIsAlternative = function(genre) {
        if (genre == 'Alternative') {
            return true;
        }
        return false;
    }

    $scope.genreIsCountryFolk= function(genre) {
        if (genre == 'Country/Folk') {
            return true;
        }
        return false;
    }

    $scope.genreIsClassicRock = function(genre) {
        if (genre == 'Classic Rock') {
            return true;
        }
        return false;
    }

    $scope.genreIsClassical = function(genre) {
        if (genre == 'Classical') {
            return true;
        }
        return false;
    }

    $scope.genreIsJazz = function(genre) {
        if (genre == 'Jazz') {
            return true;
        }
        return false;
    }

    $scope.genreIsHipHop = function(genre) {
        if (genre == 'Hip-Hop') {
            return true;
        }
        return false;
    }


    $scope.genreIsClassical = function(genre) {
        if (genre == 'Classical') {
            return true;
        }
        return false;
    }

    $scope.genreIsRap = function(genre) {
        if (genre == 'Rap') {
            return true;
        }
        return false;
    }

    $scope.genreIsOther = function(genre) {
        if (genre == 'Other') {
            return true;
        }
        return false;
    }


    $scope.increment = function(counter) {
        counter = counter + 1;
        return counter;
    }

    
    $scope.genreFilter = function(genre) {
        if ($scope.genreIncludes.length > 0) {
            if ($.inArray(genre.genre, $scope.genreIncludes) < 0)
                return;
        }
        
        return genre;
    }
    $scope.continueListingDown = function() {
      
      console.log(counter);
      console.log("dat jawn doe");
      if (counter >= 5) {
        return true;
      }
      else {
        counter = counter + 1;
        return false;
      }
      
    }

    $scope.refreshList = function() {
      counter = 0;
      console.log("refreshing");
      console.log(countOfList);
      return;
    }
}
