Admin = ($scope, $http) ->
  $scope.save = ->
    $http.post '_s/page', angular.toJson($scope.page)

# Angular bootstrap
name = 'AdminPage'
app = angular.module name, []
app.controller 'Admin', Admin
angular.bootstrap document, [name]