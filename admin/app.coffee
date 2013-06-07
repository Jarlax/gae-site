@file_obj = null

Admin = ($scope, $http) ->
  $scope.put = ->
    $http
      method: 'PUT',
      url: '_s/page/' + $scope.page.id,
      headers:
        'Content-Type': false
      transformRequest: (data) ->
        formData = new FormData()
        formData.append 'data', angular.toJson data.page
        if data.file
          formData.append 'file', data.file
        formData
      data:
        page: $scope.page
        file: file_obj
  $scope.delete = ->
    $http.delete '_s/page/' + $scope.page.id
  $scope.get = ->
    $http.get('_s/page/' + $scope.page.id).success (resp) ->
      $scope.page = resp

# Angular bootstrap
name = 'AdminPage'
app = angular.module name, []
app.controller 'Admin', Admin
angular.bootstrap document, [name]