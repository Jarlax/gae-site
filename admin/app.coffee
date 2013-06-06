@image_file = null

Admin = ($scope, $http) ->
  submit = (method, url) ->
    $http
      method: method,
      url: url,
      headers:
        'Content-Type': false
      transformRequest: (data) ->
        formData = new FormData()
        formData.append 'data', angular.toJson data.page
        if data.image
          formData.append 'image', data.image
        formData
      data:
        page: $scope.page
        image: image_file

  $scope.id = 'test'
  $scope.page =
    name: '1',
    content: '2'
  $scope.post = ->
    submit 'POST', '_s/page'
  $scope.put = ->
    submit 'PUT', '_s/page/' + $scope.id
  $scope.delete = ->
    $http.delete '_s/page/' + $scope.id
  $scope.get = ->
    $http.get('_s/page/' + $scope.id).success (resp) ->
      $scope.page = resp

# Angular bootstrap
name = 'AdminPage'
app = angular.module name, []
app.controller 'Admin', Admin
angular.bootstrap document, [name]