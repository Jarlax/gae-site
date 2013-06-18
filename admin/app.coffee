@file_obj = null

@drag = (ev) ->
  ev.dataTransfer.setData "Text", "![](/file/" + ev.target.id + ")"

@drop = (ev) ->
  ev.preventDefault()
  el = ev.target
  el.value += ev.dataTransfer.getData "Text"

@allowDrop = (ev) ->
  ev.preventDefault()

Admin = ($scope, $http) ->
  $scope.converter = new Showdown.converter();
  $scope.templates =
    'text': {title:'Text Post', icon:'icon-pencil'},
    'img': {title:'Image', icon:'icon-picture'},
    'img_coll': {title:'Image Collection', icon:'icon-th-large'}
  $http.get('_s/logout-url').success (url) ->
    $scope.logout_url = url
  list = ->
    $http.get('_s/pages').success (data) ->
      $scope.pages = data
      $scope.$apply();
  list()
  $scope.createPage = (val) ->
    $scope.page =
      template: val
  $scope.getIcon = (templ) ->
    $scope.templates[templ].icon
  $scope.put = ->
    $http(
      method: 'PUT',
      url: '_s/page/' + $scope.page.id,
      headers:
        'Content-Type': false
      transformRequest: (data) ->
        data.page.content_html = $scope.converter.makeHtml(data.page.content || '')
        formData = new FormData()
        formData.append 'data', angular.toJson data.page
        if data.file
          formData.append 'file', data.file
        formData
      data:
        page: $scope.page
        file: file_obj).success -> list()
  $scope.delete = (id) ->
    $http.delete('_s/page/' + id).success ->
      list()
  $scope.get = (id) ->
    $http.get('_s/page/' + id).success (resp) ->
      $scope.page = resp

# Angular bootstrap
name = 'AdminPage'
app = angular.module name, []
app.controller 'Admin', Admin
angular.bootstrap document, [name]