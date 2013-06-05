Admin = ($scope, $http) ->
  $scope.key = 'test'
  $scope.post = ->
    $http.post '_s/page', angular.toJson($scope.page)
  $scope.put = ->
    $http.put '_s/page/' + $scope.key, angular.toJson($scope.page)
  $scope.delete = ->
    $http.delete '_s/page/' + $scope.key
  $scope.get = ->
    $http.get('_s/page/' + $scope.key).success (resp) ->
      $scope.page = resp

# Angular bootstrap
name = 'AdminPage'
app = angular.module name, []
app.controller 'Admin', Admin
angular.bootstrap document, [name]