var WGMOVELOCK = 0;
//jQuery.fx.interval = 20; // 50fps.

var MAP = $("#map");
function wgTile(pos, items) {
    this.dom = $(document.createElement("div"));
    this.position = pos;
    this.dom.css("left", pos[0]*32).css("top", (pos[1]-pos[2])*32);
    this.items = items;
    for(var i = 0; i < items.length; i++) {
        this.dom.append(items[i]);
    }
    return this;
}

function wgFullRender() {
    // XXX: 25x17 static map now.
    //map.find("*").remove();

    for(var x = 0; x < 25; x++) {
        for(var y = 0; y < 17; y++) {
            var elm = $(document.createElement('div'));
            MAP.append(wgTile([x, y, 0], [elm]).dom);
            if(x == 10 && y == 10) {
                elm.wgItemSprite(1454);
            } else if(x == 8 && y == 8) {
                elm.wgAnimateOutfit(27, {'delay':0.3, 'start':2, 'repeat': true});
            } else {
                elm.wgItemSprite(3031);
            }

          
        }
    }
}
function wgGetTileByView(viewX, viewY) {
    fields = MAP.find('div');
    length = fields.length;
    var rX = (viewX * 32) + 'px';
    var rY = (viewY * 32) + 'px';
    while(length--) {
        if(fields[length].style.left == rX && fields[length].style.left == rY)
            return $(fields[length]); 
    }
}
// To be moved.
function wgReleaseMoveLock() {
    WGMOVELOCK = 0;
}
function wgMoveLeft() {
    if(WGMOVELOCK) return;
    WGMOVELOCK = 1;
    
    for(var y = 0; y < 16; y++) {
        var elm = $(document.createElement('div'));
        MAP.append(wgTile([-1, y, 0], [elm]).dom);
        
    }
    var fields = MAP.children();

    MAP.animate({"left": "+=32px"}, {"duration": 320, easing: 'linear', queue: false, complete: function() {
        wgReleaseMoveLock();
        fields.each(function() { 
            var elm = $(this);
            var left = parseInt(elm.css("left"));
            if(left >= 480) {
                elm.remove();
            } else {
                elm.css("left", left+32);
            }
        }); 
        MAP.css("left", 0);
       
    }});
}
function wgMoveRight() {
    if(WGMOVELOCK) return;
    WGMOVELOCK = 1;

    for(var y = 0; y < 16; y++) {
        var elm = $(document.createElement('div'));
        MAP.append(wgTile([16, y, 0], [elm]).dom);

    }
    var fields = MAP.children();

    MAP.animate({"left": "-=32px"}, {"duration": 320, easing: 'linear', queue: false, complete: function() {
        wgReleaseMoveLock();
        fields.each(function() {
            var elm = $(this);
            var left = parseInt(elm.css("left"));
            if(left < 32) {
                elm.remove();
            } else {
                elm.css("left", left-32);
            }
        });
        MAP.css("left", 0);

    }});

}
function wgMoveUp() {
    if(WGMOVELOCK) return;
    WGMOVELOCK = 1;

    for(var x = 0; x < 16; x++) {
        var elm = $(document.createElement('div'));
        MAP.append(wgTile([x, -1, 0], [elm]).dom);

    }
    var fields = MAP.children();

    MAP.animate({"top": "+=32px"}, {"duration": 320, easing: 'linear', queue: false, complete: function() {
        wgReleaseMoveLock();
        fields.each(function() {
            var elm = $(this);
            var top = parseInt(elm.css("top"));
            if(top >= 480) {
                elm.remove();
            } else {
                elm.css("top", top+32);
            }
        });
        MAP.css("top", 0);

    }});
}
function wgMoveDown() {
    if(WGMOVELOCK) return;
    WGMOVELOCK = 1;
    
    for(var x = 0; x < 16; x++) {
        var elm = $(document.createElement('div'));
        MAP.append(wgTile([x, 16, 0], [elm]).dom);

    }
    var fields = map.children();

    MAP.animate({"top": "-=32px"}, {"duration": 320, easing: 'linear', queue: false, complete: function() {
        wgReleaseMoveLock();
        fields.each(function() {
            var elm = $(this);
            var top = parseInt(elm.css("top"));
            if(top < 32) {
                elm.remove();
            } else {
                elm.css("top", top-32);
            }
        });
        MAP.css("top", 0);

    }});
}

