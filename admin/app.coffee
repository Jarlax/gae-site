Admin = ($scope, $http) ->
  $scope.converter = new Showdown.converter();
  load_menu = ->
    $http.get('_menu').success (html) ->
      $scope.menu = html
  load_menu()

# Angular bootstrap
name = 'AdminPage'
app = angular.module name, []
app.controller 'Admin', Admin
angular.bootstrap document, [name]