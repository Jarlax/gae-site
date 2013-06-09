@file_obj = null

Admin = ($scope, $http) ->
  $scope.templates = [
    {id:'main', title:'Main Site Entry', icon:'icon-home'},
    {id:'blog', title:'Blog Post', icon:'icon-pencil'},
    {id:'img', title:'Image', icon:'icon-picture'},
    {id:'img_coll', title:'Image Collection', icon:'icon-th-large'}
  ]
  $http.get('_s/logout-url').success (url) ->
    $scope.logout_url = url
  list = ->
    $http.get('_s/pages').success (data) ->
      $scope.pages = data
  list()
  $scope.createPage = (val) ->
    alert val
  $scope.put = ->
    $http(
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
        file: file_obj).success -> list()
  $scope.delete = ->
    $http.delete('_s/page/' + $scope.page.id).success = ->
      list()
  $scope.get = ->
    $http.get('_s/page/' + $scope.page.id).success (resp) ->
      $scope.page = resp

# Angular bootstrap
name = 'AdminPage'
app = angular.module name, []
app.controller 'Admin', Admin
angular.bootstrap document, [name]