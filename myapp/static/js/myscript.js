const NEW_PAGE_ID = 0;

// Handsontableの使い方
// http://qiita.com/opengl-8080/items/ac19deec388c357cd498
// http://qiita.com/opengl-8080/items/9d25e106ff48b66cb908
var data = [];

var grid = document.getElementById('grid');

var table = new Handsontable(grid, {
    data: data,
    
    // データバインディングするときはdataSchema設定が必要だが、
    // columnsで指定すれば、dataSchemaによる設定は不要っぽい
    // http://qiita.com/kivatek/items/c839bdb09e75537b15f8
    // dataSchema: {
    //     purchase_date: null,
    //     name: null,
    //     price: null,
    // },
    columns: [
        { data: 'purchase_date', type: 'text' },
        { data: 'name', type: 'text' },
        { data: 'price', type: 'numeric' },
    ],
    
    // 列ヘッダを表示
    colHeaders: ["日付", "名前", "価格"],
    // 行ヘッダを表示(1からの連番)
    rowHeaders: true,
    // 列幅
    colWidths: [120, 200, 100]
});

// アロー関数で即時実行
// http://analogic.jp/arrow-function/#immediate-function
var id = (() => {
    // https://syncer.jp/javascript-reference/location
    var found = location.pathname.match(/\/myapp\/records\/(.*?)\/edit$/);
    // 新規作成の時は、便宜上id=0とみなして処理する
    return found ? found[1] : NEW_PAGE_ID;
})();


// -----------------------------------
// Handsontableのhooks設定
// -----------------------------------
Handsontable.hooks.add('onAddRow', mydata => {
    // 行の追加
    table.alter('insert_row', data.length);
});

Handsontable.hooks.add('onSave', mydata => {
    // 保存時の処理
    // CSRF対策のCookieを取得する
    // https://docs.djangoproject.com/en/1.10/ref/csrf/#ajax
    var csrftoken = Cookies.get('csrftoken');
    
    // Djangoのdjango.middleware.csrf.CsrfViewMiddlewareを使っているため、
    // POST時にmodeとcredentialsとX-CSRFTokenヘッダを付ける
    fetch(`/myapp/ajax/records/${id}`, {
        method: 'POST',
        headers: {
            'content-type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        mode: 'same-origin',
        credentials: 'same-origin',
        body: JSON.stringify(mydata),
    }).then(response => {
        console.log(response.url, response.type, response.status);

        if (response.status == '200'){
            window.alert('保存しました');
            // 一覧にリダイレクト
            location.href = '/myapp/records';
        }
        else{
            window.alert('保存できませんでした');
        }
    }).catch(err => console.error(err));
});


// -----------------------------------
// イベントリスナーの追加
// -----------------------------------
document.addEventListener("DOMContentLoaded", () => {
    // loadした時に、Handsontableの初期値を取得・表示
    fetch(`/myapp/ajax/records/${id}`, {
        method: 'GET',
    }).then(response => {
        console.log(response.url, response.type, response.status);

        response.json().then(json => {
            for (var i = 0; i < json.length; i++){
                data.push({
                    purchase_date: json[i].purchase_date,
                    name: json[i].name,
                    price: json[i].price,
                });
            }

            table.render();
        });
    }).catch(err => console.error(err));
}, false);

document.getElementById('save').addEventListener('click', () => {
    // 保存ボタンを押したときに発火するHandsontableのhook
    Handsontable.hooks.run(table, 'onSave', data);
});

document.getElementById('add').addEventListener('click', () => {
    // 行追加を押したときに発火するHandsontableのhook
    Handsontable.hooks.run(table, 'onAddRow', data);
});