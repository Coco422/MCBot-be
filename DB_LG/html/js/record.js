let mediaRecorder;
let audioChunks = [];
let isRecording = false;

// 获取用户麦克风权限并开始录音
document.getElementById('record_button').addEventListener('click', async () => {
    const button = document.getElementById('record_button');

    if (!isRecording) {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = (event) => {
                audioChunks.push(event.data);
            };
            mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                await record_voice(audioBlob);
                audioChunks = []; // 清空录音数据
            };
            mediaRecorder.start();

            document.getElementById('record_button').style.backgroundColor = "red";
            isRecording = true;
            button.innerText = "停";
            // document.getElementById('result').innerText = "录音中...";
        } catch (error) {
            console.error("无法访问麦克风:", error);
            document.getElementById('result').innerText = "无法访问麦克风，请检查权限。";
        }
    } else {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
            isRecording = false;
            button.innerText = "录";
            document.getElementById('record_button').style.backgroundColor = "#007bff";
        }
    }
});
// 语言识别输入
function record_voice(audioBlob) {
    console.log("开始识别", audioBlob);

    // 创建 FormData 对象
    const formData = new FormData();
    formData.append("file", audioBlob, "recording.wav"); // 添加 Blob 到 FormData
    formData.append('model', 'FunAudioLLM/SenseVoiceSmall');

    // 发送请求
    axios.post(`https://nlp-demo.szmckj.cn/api/asr`, formData, {
        headers: {
            "Content-Type": "multipart/form-data", // 设置请求头
        },
    })
        .then(response => {
            console.log("识别结果:", response.data);
            document.getElementById('chat-input').innerText = response.data.text;
        })
        .catch(error => {
            console.error("识别失败:", error);
        });
}