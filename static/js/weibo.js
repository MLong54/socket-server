var apiWeiboAll = function(callback) {
    var path = '/api/weibo/all'
    ajax('GET', path, '', callback)
}

var apiWeiboAdd = function(form, callback) {
    var path = '/api/weibo/add'
    ajax('POST', path, form, callback)
}

var apiWeiboDelete = function(weibo_id, callback) {
    var path = `/api/weibo/delete?id=${weibo_id}`
    ajax('GET', path, '', callback)
}

var apiWeiboUpdate = function(form, callback) {
    var path = '/api/weibo/update'
    ajax('POST', path, form, callback)
}

var apiCommentAdd = function(form, callback) {
    var path = '/api/comment/add'
    ajax('POST', path, form, callback)
}

var apiCommentDelete = function(comment_id, callback) {
    var path = `/api/comment/delete?id=${comment_id}`
    ajax('GET', path, '', callback)
}

var apiCommentUpdate = function(form, callback) {
    var path = '/api/comment/update'
    ajax('POST', path, form, callback)
}

//  weibo 模板字符串
var weiboTemplate = function(weibo) {
    var w = `
        <hr>
        <div class="weibo-cell" data-id="${weibo.id}">
            <p>
                <span class="weibo-username">${weibo.user_name}</span>
                <span> : </span>
                <span class="weibo-content">${weibo.content}</span>
                <button class="weibo-delete">删除</button>
                <button class="weibo-edit">编辑</button>
            </p>
    `
    return w
}

//  comment 模板字符串
var commentTemplate = function(comment) {
    var c = `
        <div class="comment-cell" data-id="${comment.id}">
            <span class="comment-username">${comment.user_name}</span>
            <span> : </span>
            <span class="comment-content">${comment.content}</span>
            <button class="comment-delete">删除</button>
            <button class="comment-edit">编辑</button>
        </div>
    `
    return c
}

//  commentAdd 模板字符串
var commentAddTemplate = function() {
    var c = `
        <div class="comment-add-form">
            <input class="comment-add-input" value="">
            <br>
            <button class="comment-add">添加评论</button>
        </div>
    `
    return c
}

 //  weiboUpdate 模板字符串
var weiboUpdateTemplate = function(content) {
    var w = `
        <div class="weibo-update-form">
            <p>
                <input class="weibo-update-input" value="${content}">
                <button class="weibo-update">更新</button>
            </p>
        </div>
    `
    return w
}

 //  commentUpdate 模板字符串
var commentUpdateTemplate = function(content) {
    var w = `
        <div class="comment-update-form">
            <p>
                <input class="comment-update-input" value="${content}">
                <button class="comment-update">更新</button>
            </p>
        </div>
    `
    return w
}

// 插入新增 weibo
var insertWeibo = function(weibo) {
    var weiboCell = weiboTemplate(weibo)
    var commentAddForm = commentAddTemplate(weibo)
    weiboCell += commentAddForm
    var weiboList = e('#id-weibo-list')
    weiboList.insertAdjacentHTML('beforeend', weiboCell)
}

// 插入新增 comment
var insertComment = function(comment, weiboCell) {
    var commentAddForm = e('.comment-add-form', weiboCell)
    var commentCell = commentTemplate(comment)
    commentAddForm.insertAdjacentHTML('beforebegin', commentCell)
}

// 插入 weibo 更新模板
var insertWeiboUpdateForm = function(content, weiboCell) {
    var updateForm = weiboUpdateTemplate(content)
    weiboCell.insertAdjacentHTML('beforeend', updateForm)
}

// 插入 comment 更新模板
var insertCommentUpdateForm = function(content, commentCell) {
    var updateForm = commentUpdateTemplate(content)
    commentCell.insertAdjacentHTML('beforeend', updateForm)
}



// 加载带评论的 weibo
var loadWeibos = function() {
    apiWeiboAll(function(weibos) {
        log('load all weibos', weibos)
        // 通过循环将 weibo 添加到页面中
        var commentAddForm = commentAddTemplate()
        for(var i = 0; i < weibos.length; i++) {
            var weibo = weibos[i]
            var weiboCell = weiboTemplate(weibo)
            var weiboList = e('#id-weibo-list')

            // 用循环遍历该 weibo 对象的 comments 来构造评论模板字符串
            var comments = weibo.comments
            for(var j = 0; j < comments.length; j++) {
                var comment = comments[j]
                commentCell = commentTemplate(comment)
                // 用拿到的评论模板字符串和之前的微博模板字符串合并
                weiboCell += commentCell
            }
            // 模板字符串再次合并
            weiboCell += commentAddForm
            // insert 整个合并后的模板字符串
            weiboList.insertAdjacentHTML('beforeend', weiboCell)
        }
    })
}

var bindEventWeiboAdd = function() {
    var b = e('#id-button-add')
    // 注意, 第二个参数可以直接给出定义函数
    b.addEventListener('click', function(){
        var userId = b.dataset['id']
        var input = e('#id-input-weibo')
        var content = input.value
        log('click add weibo', content)
        var form = {
            content: content,
        }
        apiWeiboAdd(form, function(weibo) {
            // 收到返回的数据, 插入到页面中
            insertWeibo(weibo)
            input.value = ''
        })
    })
}


var bindEventWeiboDelete = function() {
    var weiboList = e('#id-weibo-list')
    // 事件响应函数会传入一个参数 就是事件本身
    weiboList.addEventListener('click', function(event) {
    // 我们可以通过 event.target 来得到被点击的对象
    var self = event.target
    log('被点击的元素', self)
    // 通过比较被点击元素的 class
    // 来判断元素是否是我们想要的
    // classList 属性保存了元素所有的 class
    log(self.classList)
    if (self.classList.contains('weibo-delete')) {
        log('点到了删除按钮')
        var weiboId = self.closest('.weibo-cell').dataset['id']

        apiWeiboDelete(weiboId, function(r) {
            /// 验证权限
            if (r.deny) {
            alert(r.message)
            } else {
            log('apiWeiboDelete', r.message)
            self.closest('.weibo-cell').remove()
            alert(r.message)
            }
        })
    } else {
        log('点到了 weibo cell')
    }
})}

var bindEventWeiboEdit = function() {
    var weiboList = e('#id-weibo-list')
    // 事件响应函数会传入一个参数 就是事件本身
    weiboList.addEventListener('click', function(event) {
    log(event)
    // 我们可以通过 event.target 来得到被点击的对象
    var self = event.target
    log('被点击的元素', self)
    // 通过比较被点击元素的 class
    // 来判断元素是否是我们想要的
    // classList 属性保存了元素所有的 class
    log(self.classList)
    if (self.classList.contains('weibo-edit')) {
        log('点到了编辑按钮')
        var weiboPart = self.parentElement
        var weiboCell = self.closest('.weibo-cell')
        var weiboId = weiboCell.dataset['id']
        var weiboContent = e('.weibo-content', weiboPart)
        var content = weiboContent.innerText
        // 插入编辑输入框
        insertWeiboUpdateForm(content, weiboPart)
    } else {
        log('点到了 weibo cell')
    }
})}

var bindEventWeiboUpdate = function() {
    var weiboList = e('#id-weibo-list')
    // 事件响应函数会传入一个参数 就是事件本身
    weiboList.addEventListener('click', function(event) {
    log(event)
    // 我们可以通过 event.target 来得到被点击的对象
    var self = event.target
    log('被点击的元素', self)
    // 通过比较被点击元素的 class
    // 来判断元素是否是我们想要的
    // classList 属性保存了元素所有的 class
    log(self.classList)
    if (self.classList.contains('weibo-update')) {
        log('点到了更新按钮')
        var weiboCell = self.closest('.weibo-cell')
        var weiboId = weiboCell.dataset['id']
        log('update weibo id', weiboId)
        var input = e('.weibo-update-input', weiboCell)
        var content = input.value
        var form = {
            id: weiboId,
            content: content,
        }

        apiWeiboUpdate(form, function(r) {
            var updateForm = e('.weibo-update-form', weiboCell)
            updateForm.remove()
            /// 验证权限
            if (r.deny) {
            alert(r.message)
            } else {
            weibo = r
            var weiboContent = e('.weibo-content', weiboCell)
            weiboContent.innerText = weibo.content
            }
        })
    } else {
        log('点到了 weibo cell')
    }
})}

// 绑定添加评论事件
var bindEventCommentAdd = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
    var self = event.target
    if (self.classList.contains('comment-add')) {
        var weiboCell = self.closest('.weibo-cell')
        var weiboId = weiboCell.dataset['id']
        var input = e('.comment-add-input', weiboCell)
        var commentContent = input.value
        var form = {
            weibo_id: weiboId,
            content: commentContent,
        }

        apiCommentAdd(form, function(comment) {
            insertComment(comment, weiboCell)
            input.value = ''
        })
    } else {
        log('点到了 weibo cell')
    }
})}

// 绑定删除评论事件
var bindEventCommentDelete = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
    var self = event.target
    if (self.classList.contains('comment-delete')) {
        var commentCell = self.closest('.comment-cell')
        var commentId = commentCell.dataset['id']

        apiCommentDelete(commentId, function(r) {
            /// 验证权限
            if (r.deny) {
            alert(r.message)
            } else {
            log('apiCommentDelete', r.message)
            self.parentElement.remove()
            alert(r.message)
            }
        })
    } else {
        log('点到了 weibo cell')
    }
})}

// 绑定编辑评论事件
var bindEventCommentEdit = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
    var self = event.target
    if (self.classList.contains('comment-edit')) {
        var commentCell = self.closest('.comment-cell')
        var ommentId = commentCell.dataset['id']
        var commentContent = e('.comment-content', commentCell)
        var content = commentContent.innerText
        insertCommentUpdateForm(content, commentCell)
    } else {
        log('点到了 weibo cell')
    }
})}

// 绑定更新评论事件
var bindEventCommentUpdate = function() {
    var weiboList = e('#id-weibo-list')
    weiboList.addEventListener('click', function(event) {
    var self = event.target
    if (self.classList.contains('comment-update')) {
        var commentCell = self.closest('.comment-cell')
        var commentId = commentCell.dataset['id']
        var input = e('.comment-update-input', commentCell)
        var content = input.value
        var form = {
            id: commentId,
            content: content,
        }

        apiCommentUpdate(form, function(r) {
            var updateForm = e('.comment-update-form', commentCell)
            updateForm.remove()
            /// 验证权限
            if (r.deny) {
            alert(r.message)
            } else {
            comment = r
            var commentContent = e('.comment-content', commentCell)
            commentContent.innerText = comment.content
            }

        })
    } else {
        log('点到了 weibo cell')
    }
})}

var bindEvents = function() {
    bindEventWeiboAdd()
    bindEventWeiboDelete()
    bindEventWeiboEdit()
    bindEventWeiboUpdate()
    bindEventCommentAdd()
    bindEventCommentDelete()
    bindEventCommentEdit()
    bindEventCommentUpdate()
}

var __main = function() {
    bindEvents()
    loadWeibos()
}

__main()
