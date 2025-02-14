let mediaRecorder;
let audioChunks = [];

// 显示录音和停止录音的消息
function showMessage(message, type = 'warning') {
    const styles = {
        warning: {
            bg: '#fdf6ec',
            color: '#e6a23c',
            border: '#faecd8'
        },
        success: {
            bg: '#f0f9eb',
            color: '#67c23a',
            border: '#e1f3d8'
        },
        error: {
            bg: '#fef0f0',
            color: '#f56c6c',
            border: '#fde2e2'
        }
    };

    const currentStyle = styles[type] || styles.warning;

    const messageDiv = document.createElement('div');
    messageDiv.style.cssText = `
      position: fixed;
      top: 40px;
      left: 50%;
      transform: translateX(-50%);
      padding: 10px 20px;
      border-radius: 4px;
      background-color: ${currentStyle.bg};
      color: ${currentStyle.color};
      border: 1px solid ${currentStyle.border};
      z-index: 9999;
      transition: opacity 0.3s;
      font-size: 14px;
  `;
    messageDiv.textContent = message;
    document.body.appendChild(messageDiv);

    // 3秒后自动消失
    setTimeout(() => {
        messageDiv.style.opacity = '0';
        setTimeout(() => {
            document.body.removeChild(messageDiv);
        }, 300);
    }, 2000);
}

// 获取用户媒体权限
navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
        mediaRecorder = new MediaRecorder(stream);

        // 录音数据可用时触发
        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };
        // 录音停止时触发
        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
            const audioUrl = URL.createObjectURL(audioBlob);
            console.log("录音完成，URL:", audioUrl);

            // 创建音频播放器
            const audioPlayer = document.createElement("audio");
            audioPlayer.controls = true;
            audioPlayer.src = audioUrl;
            document.getElementById("audio-player").innerHTML = "";
            document.getElementById("audio-player").appendChild(audioPlayer);

            // 启用上传按钮
            document.getElementById("upload-record").disabled = false;
        };
    })
    .catch(error => {
        console.error("无法获取麦克风权限:", error);
    });

// 开始录音
document.getElementById("start-record").addEventListener("click", () => {
    console.log("开始录音");
    this.showMessage("开始录音", "success");
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();
            // document.getElementById('start-record').disabled = true;
            // document.getElementById('stop-record').disabled = false;

            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const audioUrl = URL.createObjectURL(audioBlob);
                document.getElementById('audioPlayback').src = audioUrl;
            };
        });
});

// 停止录音
function stopRecord() {
    mediaRecorder.stop();
    // document.getElementById("stop-record").disabled = true;
    // document.getElementById("start-record").disabled = false;
    console.log("停止录音");
    this.showMessage("停止录音", "error");
}

// 重新录音
document.getElementById("restart-record").addEventListener("click", () => {
    audioChunks = [];
    document.getElementById('audioPlayback').src = "";
    // document.getElementById('restart-record').disabled = true;
    console.log("重新录音");
    this.showMessage("重新录音", "warning");
});


// 生成录音
document.getElementById("upload_audio_button").addEventListener("click", async () => {
    if (audioChunks.length === 0) {
        alert("请先录制音频！");
        return;
    }
    this.showMessage("音频生成中，请稍后......", "success");
    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
    const reader = new FileReader();
    reader.readAsDataURL(audioBlob);
    reader.onloadend = async () => {
        const base64Audio = reader.result.split(',')[1];
        const response = await fetch('/api/clone-voice', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                custom_name: "UserVoice",
                reference_text: document.getElementById('AI_text').textContent,
                base64_audio: base64Audio,
                tts_text: document.getElementById('user_text').value
            })
        });
        const audioData = await response.blob();
        const audioUrl = URL.createObjectURL(audioData);

        // const audio = new Audio(audioUrl);
        // audio.play();

        // 创建新的音频播放器

        const audioPlayer = document.createElement('audio');
        audioPlayer.src = audioUrl;
        audioPlayer.controls = true; // 添加控制条
        audioPlayer.style.marginTop = '10px'; // 添加一些样式

        // 将音频播放器插入到页面中
        const container = document.getElementById('audio-player-container'); // 假设你有一个容器来存放播放器
        container.appendChild(audioPlayer);

        // 自动播放音频
        audioPlayer.play();
    };
});