// update_product
window.addEventListener('load', function () {
    document.getElementById('btn_update_product') && document.getElementById('btn_update_product').addEventListener('click', updateProductStart);
    document.getElementById('btn_long_task') && document.getElementById('btn_long_task').addEventListener('click', start_long_task);
    document.getElementById('btn_long_task_nanobar') && document.getElementById('btn_long_task_nanobar').addEventListener('click', start_long_task_nanobar);
});


function updateProductStart() {
    const product = this.dataset.product;
    const url = this.dataset.link + '?product=' + product;

    stilizationUpdateBlocked(this)
    // alert(`Старт обновления!\n\t${url}\n\tproduct = ${product}`);

    // window.location.href = url;
    sendUpdateAjax(url, 'start');
}

function sendUpdateAjax(url, command) {
    states_dictionary={
        idle: 'не запущено',
        update: 'обновляется',
        finish: 'завершено',
    };
    fetch(url, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({command: command})
    })
        .then(resp => resp.json())
        // .then(resp => console.log(resp))
        .then(resp => {
            // console.log(resp.errors)
            if (typeof resp.errors !== 'undefined') {
                setUpdateStatus('ошибка: ' + resp.errors[0]);
                stilizationUpdateReset(this);
            } else {
                console.log(resp);
                stat = states_dictionary[resp.process];
                setUpdateStatus(stat);
            }
        })
        .catch(() => {
            // console.log('ошибка');
            setUpdateStatus('ошибка');
            stilizationUpdateReset(this);
        });
}

function stilizationUpdateBlocked(el) {
    el.disabled = true;
    el.classList.remove('btn-danger');
    el.classList.add('btn-outline-danger');
}

function stilizationUpdateFinish(el) {
    stilizationUpdateReset(el)
    setUpdateStatus('завершено')
}

function stilizationUpdateReset(el) {
    el.disabled = false;
    el.classList.remove('btn-outline-danger');
    el.classList.add('btn-danger');
}

function setUpdateStatus(status) {
    document.getElementById('update_status').textContent = status
}

function outputUpdateInfo(info) {
    document.getElementById('update_info').textContent = info
}


// go top button
window.addEventListener('load', function () {
    const goTopBtn = document.querySelector('.go-top-btn');
    window.addEventListener('scroll', trackScroll);
    goTopBtn.addEventListener('click', goTop);

    function trackScroll() {
        const scrolled = window.scrollY;
        const coords = document.documentElement.clientHeight;
        if (scrolled > (coords / 3)) {
            goTopBtn.classList.add('go-top-btn--show');
        } else {
            goTopBtn.classList.remove('go-top-btn--show');
        }
        // window.scrollY > document.documentElement.clientHeight ? goTopBtn.classList.add('go-top-btn--show') : goTopBtn.classList.remove('go-top-btn--show');
    }

    function goTop() {
        if (window.scrollY > 0) {
            // window.scrollBy(0, -10000);  // второй аргумент - на сколько прокручивать за шаг (скорость)
            // setTimeout(goTop, 0);
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
        // window.scrollY > 0 && (window.scrollBy(0, -700), setTimeout(goTop, 0));
    }
});


// long_task, progress - nanobar
function start_long_task_nanobar() {
    div = $('<div class="progress-bar"><div></div><div class="me-2">0%</div><div class="me-2">...</div><div>&nbsp;</div></div><hr>');
    $('#progress').append(div);

    var nanobar = new Nanobar({
        bg: '#44f',
        target: div[0].childNodes[0]
    });

    $.ajax({
        type: 'POST',
        url: '/longtask',
        success: function(data, status, request) {
            status_url = request.getResponseHeader('Location');
            update_progress_nanobar(status_url, nanobar, div[0]);
        },
        error: function() {
            alert('Unexpected error');
        }
    });
}

function update_progress_nanobar(status_url, nanobar, status_div) {
    // send GET request to status URL
    $.getJSON(status_url, function(data) {
        // update UI
        percent = parseInt(data['current'] * 100 / data['total']);
        nanobar.go(percent);
        $(status_div.childNodes[1]).text(percent + '%');
        $(status_div.childNodes[2]).text(data['status']);
        if (data['state'] != 'PENDING' && data['state'] != 'PROGRESS') {
            if ('result' in data) {
                // show result
                $(status_div.childNodes[3]).text('Result: ' + data['result']);
            }
            else {
                // something unexpected happened
                $(status_div.childNodes[3]).text('Result: ' + data['state']);
            }
        }
        else {
            // rerun in 2 seconds
            setTimeout(function() {
                update_progress_nanobar(status_url, nanobar, status_div);
            }, 2000);
        }
    });
}


// long_task
function start_long_task() {
    {/*
    <div class="progress" role="progressbar" aria-label="Basic example" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100">
        <div class="progress-bar w-75"></div>
    </div>
    */}

    // div = $('<div class="progress-bar"><div></div><div class="me-2">0%</div><div class="me-2">...</div><div>&nbsp;</div></div><hr>');
    // $('#progress').append(div);

    var el_progress = document.getElementById('progress')
    var progress = document.createElement('div');
    progress.className = 'progress mb-3';
    progress.setAttribute('role', 'progressbar');
    progress.setAttribute('aria-label', 'Basic example');
    progress.setAttribute('aria-valuemin', '0');
    progress.setAttribute('aria-valuemax', '100');
    progress.setAttribute('aria-valuenow', '0');

    var bar = document.createElement('div');
    bar.className = 'progress-bar progress-bar-striped progress-bar-animated';
    bar.style.width = '0%';
    progress.append(bar);
    // div.appendChild(bar);
    el_progress.append(progress);

    // Percentage
    var percentage = document.createElement('div');
    percentage.append('0%');
    el_progress.append(percentage);

    // Status message
    var el_status = document.createElement('div');
    el_status.insertAdjacentHTML('beforeend', '<strong>Статус обновления: </strong>');
    var statusMessage = document.createElement('span');
    statusMessage.append('...');
    el_status.append(statusMessage)
    el_progress.append(el_status);

    // Result Message
    var resultMessage = document.createElement('div');
    resultMessage.insertAdjacentHTML('beforeend', '&nbsp;');
    el_progress.append(resultMessage);

    var hr = document.createElement('hr');
    el_progress.append(hr);

    $.ajax({
        type: 'POST',
        url: '/longtask',
        success: function(data, status, request) {
            status_url = request.getResponseHeader('Location');
            update_progress(status_url, bar, percentage, statusMessage, resultMessage);
        },
        error: function() {
            alert('Unexpected error');
        }
    });
}

function update_progress(status_url, bar, percentage, statusMessage, resultMessage) {
    $.getJSON(status_url, function(data) {
        percent = parseInt(data['current'] * 100 / data['total']);
        // bar.className = `progress-bar progress-bar-striped w-${percent}`;
        bar.style.width = `${percent}%`;
        bar.innerHTML = `${percent}%`;
        percentage.innerHTML = `${percent}%`;
        statusMessage.innerHTML = data['status'];

        if (data['state'] != 'PENDING' && data['state'] != 'PROGRESS') {
            if ('result' in data) {
                resultMessage.innerHTML = `Result: ${data['result']}`;
            }
            else {
                // resultMessage.innerHTML = `Result: ${data['state']}`;
                resultMessage.innerHTML = 'Result: НЕУДАЧА!';
            }
            bar.classList.remove('progress-bar-animated', 'progress-bar-striped');
        }
        else {
            setTimeout(function() {
                update_progress(status_url, bar, percentage, statusMessage, resultMessage);
            }, 2000);
        }
    });
}
