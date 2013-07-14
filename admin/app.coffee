DragDirective = ->
  (scope, element, attrs) ->
    attrs.$set('draggable', true);

    data = attrs.jxDragData
    handler = attrs.jxDrag
    endhandler = attrs.jxDragEnd

    element.bind "dragstart", (event) =>
      [dragData, dragTarget] = [data, event.target]
      event.dataTransfer.setData "text", dragData
      scope.dragTarget = dragTarget
      scope[handler]? dragData

    element.bind "dragend", =>
      scope[endhandler]?()

DropDirective = ->
  (scope, element, attrs) ->
    element.bind "dragover", (event) ->
      event.preventDefault()

    data = attrs.jxDragData
    handler = attrs.jxDrop

    element.bind "drop", (event) =>
      event.preventDefault()
      dragData = event.dataTransfer.getData "text"
      [dropData, dropTarget] = [data, event.target]
      scope.dropTarget = dropTarget
      scope[handler]? dragData, dropData

Admin = ($scope, $http, $timeout) ->
  $scope.converter = new Showdown.converter()

  $scope.drag = ->
    $scope.dragging = true

  $scope.dragend = ->
    $scope.dragging = false

  $scope.add_markdown = ->
    element = document.getElementById "content_html"
    element.value = $scope.converter.makeHtml($scope.content || '')

  $scope.drop = (from_id, to_id) ->
    from = $scope.dragTarget
    to = $scope.dropTarget
    if from != to && from_id && to_id
      $timeout ->
        $http.get("/_exchange?page1=" + from_id + "&page2=" + to_id).success ->
          [from.innerHTML, to.innerHTML] = [to.innerHTML, from.innerHTML]
        , 0.1

# Angular bootstrap
name = 'AdminPage'
app = angular.module name, []
app.controller 'Admin', Admin
app.directive 'jxDrag', DragDirective
app.directive 'jxDrop', DropDirective
angular.bootstrap document, [name]