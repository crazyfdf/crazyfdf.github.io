new Vue({
    el:'#index',
    data:{
        // topmenu:[],
        // banner:[],
        // userUI:false,
        // loginType:false,
        username:'',
        password:'',
    },
    mounted(){
      this.getData()
    },
    methods:{

        getData:function () {
            var self=this
            reqwest({
                url:'/api/index',
                method:'get',
                type:'json',
                success:function (data) {
                    //console.log(data)
                    // self.topmenu=data.topmenu
                    // self.banner=data.banner
                    // console.log(self.topmenu)
                }
            })
        },


        userLogin:function(){
          var self=this
          reqwest({
              url:'/api/index',
              method:'post',
              data:{
                  username:self.username,
                  password:self.password
              },
              headers:{
                 "X-CSRFTOKEN":csrftoken
             },
              success:function () {
                  console.log('ok')
                  if (data.loginType=='ok') {
                      self.userUI = false
                      self.loginType = true
              }
        },
              error:function (err) {
                  console.log(err)
              }
          })
        },
    //  showUserUI:function(){
    //   this.userUI = !this.userUI
    // },
    userregistration:function(){
            window.location.href = '/eva/userregistration'
    },
    userlogin:function(){
            window.location.href = '/eva/userLogin'
    },
    toeva:function() {
            window.location.href = '/eva'
    },
  }
})
