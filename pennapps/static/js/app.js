'use strict';

/* App Module */

var phonecatApp = angular.module('phonecatApp', [
  'ngRoute',
  'phonecatAnimations',

  'phonecatControllers',
  'phonecatFilters',
  'phonecatServices'
]);




phonecatApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/artists', {
        templateUrl: 'partials/phone-list.html',
        controller: 'PhoneListCtrl'
      }).
      when('/home', {
        templateUrl: 'partials/home.html',
        controller: 'PhoneListCtrl'
      }).
      when('/phones/:phoneId', {
        templateUrl: 'partials/phone-detail.html',
        controller: 'PhoneDetailCtrl'
      }).
      otherwise({
        redirectTo: '/phones'
      });
  }]);

function MyCntrl($scope) {
  $scope.lengths = [
    {name:'1 Hour'},
    {name:'2 Hours'},
    {name:'3 Hours'},
    {name:'4 Hours'},
    {name:'5 Hours'},
    {name:'6 Hours'},
    {name:'7 Hours'},    
    {name:'8 Hours'},
    {name:'9 Hours'},
    {name:'10 Hours'}
  ];
  $scope.length = $scope.lengths[3]; // 3 hours
}

var counter = 0;



phonecatApp.filter('range', function() {
  return function(input, total) {
    total = parseInt(total);
    for (var i=0; i<total; i++)
      input.push(i);
    return input;
  };
});

function Main($scope){
}    


var countOfList = $("#myList").children().length;



