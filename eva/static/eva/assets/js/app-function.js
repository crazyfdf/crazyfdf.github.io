 // {#字符流动背景#}
      var c = document.getElementById("c");
      var ctx = c.getContext("2d");
      c.height = window.innerHeight;
      c.width = window.innerWidth*0.862;
      // {#流动的字符内容#}
      var txts = "01010101010101";
      txts = txts.split("");
      var font_size = 12.5;
      var columns = c.width / font_size;
      var drops = [];
      for (var x = 0; x < columns; x++) drops[x] = 1;
      function draw() {
        ctx.fillStyle = "rgba(0, 0, 0, 0.2)";//字符长度
        ctx.fillRect(0, 0, c.width, c.height);
        ctx.fillStyle = "#00FFFF";
        ctx.font = font_size + "px arial";
        for (var i = 0; i < drops.length; i++) {
          var text = txts[Math.floor(Math.random() * txts.length)];
          ctx.fillText(text, i * font_size, drops[i] * font_size);
          if (drops[i] * font_size > c.height || Math.random() > 0.98) drops[i] = 0;
          drops[i]++;
        }
      }
      setInterval(draw, 80);




    //  // {#命运石之门0世界线变动测量仪#}
    // function toNum(num)   //以为当是个位数时，要显示01的状态#}
    // {
    //    if (num<10)
    //     {return '0'+num;}
    //    else
    //     {return ""+num;}
    //
    // }
    // window.onload=function()
    // {
    //
    //     var obj=document.getElementsByTagName("img");
    //
    //     function tick()
    //     {
    //          var time= new Date();
    //          var time1=toNum(time.getHours())+toNum(time.getMinutes())+toNum(time.getSeconds()); //获取小时分钟秒的一个字符串
    //          // console.log(time1);
    //         for (var i=0;i<8;i++)     //一个有六张图片，前两张代表小时，中间两张代表分钟，后两张代表秒，
    //             {
    //                 var j=i+4
    //                 if(i==0||i==1)
    //                 {
    //                      obj[j].src='/upload/'+time1[i]+'.png';   //时间字符串是什么，就显示什么图片
    //                 }
    //                 obj[j].src='/upload/'+time1[i]+'.png';   //时间字符串是什么，就显示什么图片
    //                 if(i==3||i==4)
    //                 {
    //                      obj[j].src='/upload/'+time1[i-1]+'.png';   //时间字符串是什么，就显示什么图片
    //                 }
    //                 if(i==6||i==7)
    //                 {
    //                      obj[j].src='/upload/'+time1[i-2]+'.png';   //时间字符串是什么，就显示什么图片
    //                 }
    //                 obj[6].src='/upload/bei1.png';
    //                 obj[9].src='/upload/bei1.png';
    //             }
    //     }
    //     window.setInterval(tick, 1000);
    //     tick();  //为了一开始不显示000000
    // }

//宇宙特效
var canvas = document.getElementById('canvas'),
ctx = canvas.getContext('2d'),
w = canvas.width = window.innerWidth,
h = canvas.height = window.innerHeight,

hue = 217,
stars = [],
count = 0,
maxStars = 60;                //星星数量,默认1300
var canvas2 = document.createElement('canvas'),
ctx2 = canvas2.getContext('2d');
canvas2.width = 100;
canvas2.height = 100;
var half = canvas2.width / 2,
gradient2 = ctx2.createRadialGradient(half, half, 0, half, half, half);
gradient2.addColorStop(0.025, '#E0FFFF');
gradient2.addColorStop(0.1, 'hsl(' + hue + ', 61%, 33%)');
gradient2.addColorStop(0.25, 'hsl(' + hue + ', 64%, 6%)');
gradient2.addColorStop(1, 'transparent');

ctx2.fillStyle = gradient2;
ctx2.beginPath();
ctx2.arc(half, half, half, 0, Math.PI * 2);
ctx2.fill();

// End cache
function random1(min, max) {
    if (arguments.length < 2) {
        max = min;
        min = 0;
    }

    if (min > max) {
        var hold = max;
        max = min;
        min = hold;
    }

    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function maxOrbit(x, y) {
    var max = Math.max(x, y),
    diameter = Math.round(Math.sqrt(max * max + max * max));
    return diameter / 2;
    //星星移动范围，值越大范围越小，
}

var Star = function() {

    this.orbitRadius = random1(maxOrbit(w, h));
    this.radius = random1(60, this.orbitRadius) / 8;       //星星大小,值越大星星越小,默认8

    this.orbitX = w / 2;
    this.orbitY = h / 2;
    this.timePassed = random1(0, maxStars);
    this.speed = random1(this.orbitRadius) / 2000000;        //星星移动速度,值越大越慢,默认5W

    this.alpha = random1(8, 10) / 10;

    count++;
    stars[count] = this;
}

Star.prototype.draw = function() {
    var x = Math.sin(this.timePassed) * this.orbitRadius + this.orbitX,
    y = Math.cos(this.timePassed) * this.orbitRadius + this.orbitY,
    twinkle = random1(0);

    if (twinkle === 1 && this.alpha > 0) {
        this.alpha -= 0.05;
    } else if (twinkle === 2 && this.alpha < 1) {
        this.alpha += 0.05;
    }

    ctx.globalAlpha = this.alpha;
    ctx.drawImage(canvas2, x - this.radius / 2, y - this.radius / 2, this.radius, this.radius);
    this.timePassed += this.speed;
}

for (var i = 0; i < maxStars; i++) {
    new Star();
}

function animation() {
    ctx.globalCompositeOperation = 'source-over';
    ctx.globalAlpha = 0.006;                                 //尾巴
    ctx.fillStyle = 'hsla(' + hue + ', 64%, 6%, 2)';
    ctx.fillRect(0, 0, w, h)

    ctx.globalCompositeOperation = 'source-atop';//source-atop
    for (var i = 1,
    l = stars.length; i < l; i++) {
        stars[i].draw();
    };

    window.requestAnimationFrame(animation);
}


animation();

// {#ai聊天#}
    function anim1_noti1(){
			Lobibox.notify('info', {
		    pauseDelayOnHover: true,
            continueDelayOnInactiveTab: false,
		    position: 'center top',
		    showClass: 'fadeInDown',
            hideClass: 'fadeOutDown',
            width: 600,
		    msg: '快来和我聊天啦~~~.'
		    });
			    //向nodejs搭建的服务器发送请求
                 $.ajax({
                     type: 'get',
                     url: 'http://127.0.0.1:8000/eva/ai',

                     success: function () {
                         console.log("开始交流")
                     },
                     error: function (err) {
                         console.log(err)
                     }
                 })
      }
