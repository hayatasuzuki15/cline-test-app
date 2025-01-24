// 現在時刻の更新
function updateClock() {
  const clockElement = document.getElementById('clock');
  const now = new Date();
  const options = {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  };
  clockElement.textContent = now.toLocaleString('ja-JP', options);
}

// 初期化時に時計を更新し、1秒ごとに更新
updateClock();
setInterval(updateClock, 1000);

// 出勤ボタンのイベントリスナー
document.getElementById('clock-in').addEventListener('click', async () => {
  try {
    const response = await fetch('/api/attendance/clock_in/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-Type': 'application/json',
      },
    });

    if (response.ok) {
      alert('出勤打刻が完了しました。');
      loadAttendanceRecords();
    } else {
      const data = await response.json();
      alert(data.detail || '出勤打刻に失敗しました。');
    }
  } catch (error) {
    console.error('Error:', error);
    alert('エラーが発生しました。');
  }
});

// 退勤ボタンのイベントリスナー
document.getElementById('clock-out').addEventListener('click', async () => {
  try {
    const response = await fetch('/api/attendance/clock_out/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-Type': 'application/json',
      },
    });

    if (response.ok) {
      alert('退勤打刻が完了しました。');
      loadAttendanceRecords();
    } else {
      const data = await response.json();
      alert(data.detail || '退勤打刻に失敗しました。');
    }
  } catch (error) {
    console.error('Error:', error);
    alert('エラーが発生しました。');
  }
});

// 勤務記録の読み込み
async function loadAttendanceRecords() {
  try {
    const response = await fetch('/api/attendance/');
    const data = await response.json();
    const recordsTable = document.getElementById('attendance-records');
    recordsTable.innerHTML = '';

    data.forEach((record) => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${new Date(record.date).toLocaleDateString('ja-JP')}</td>
        <td>${new Date(record.clock_in).toLocaleTimeString('ja-JP')}</td>
        <td>${
          record.clock_out
            ? new Date(record.clock_out).toLocaleTimeString('ja-JP')
            : '未退勤'
        }</td>
        <td>${calculateWorkDuration(record)}</td>
      `;
      recordsTable.appendChild(row);
    });
  } catch (error) {
    console.error('Error:', error);
  }
}

// 勤務時間の計算
function calculateWorkDuration(record) {
  if (!record.clock_out) return '0時間0分';

  const clockIn = new Date(record.clock_in);
  const clockOut = new Date(record.clock_out);
  const diffMs = clockOut - clockIn;
  const hours = Math.floor(diffMs / (1000 * 60 * 60));
  const minutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));

  return `${hours}時間${minutes}分`;
}

// CSRFトークンを取得する関数
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// ページ読み込み時に勤務記録を読み込む
document.addEventListener('DOMContentLoaded', loadAttendanceRecords);
