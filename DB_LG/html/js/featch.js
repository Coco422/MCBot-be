const BASE_URL = 'https://nlp-demo.szmckj.cn';
const wzyc = 'https://wzyc-demo.szmckj.cn'


const id = null;
const idA = null;
const tts_message = null;
const if_kb = false
const if_kb_ai = false
const chat_id = null;
const user_id = null
const md = null
const idtest = null
const echartsData = '1111';
// // 获取随机题目接口
// function fetchRandomQuestion() {
//     axios.get(`${BASE_URL}/api/randomquestion`)
//         .then(function (response) {
//             // 设置题目
//             document.getElementById('questionB').innerText = response.data.q_stem;
//             this.id = response.data.id;

//             // 清空选项区域
//             const optionsContainer = document.getElementById('optionsB');
//             optionsContainer.innerHTML = ''; // 清空现有选项

//             const options = response.data.options;
//             const splitData = options.split('|');

//             if (splitData.length === 2 && splitData.includes("正确") && splitData.includes("错误")) {
//                 // 如果选项是“正确|错误”格式
//                 createOption(optionsContainer, "A", "正确");
//                 createOption(optionsContainer, "B", "错误");
//             } else {
//                 // 创建一个对象来存储切分后的数据
//                 const alloptions = {};
//                 splitData.forEach(item => {
//                     const [key, value] = item.split("、"); // 根据冒号切分键值对
//                     alloptions[key] = value; // 将数据存储到对象中
//                 });

//                 // 动态生成选项
//                 createOption(optionsContainer, "A", alloptions["A"] || "无数据");
//                 createOption(optionsContainer, "B", alloptions["B"] || "无数据");
//                 createOption(optionsContainer, "C", alloptions["C"] || "无数据");
//                 createOption(optionsContainer, "D", alloptions["D"] || "无数据");
//             }
//         })
//         .catch(function (err) {
//             console.log(err);
//         });
// }

// // 获取随机题目接口 test.html2
// function TestfetchRandomQuestion() {
//     // console.log("fetchRandomQuestion");
//     axios.get(`${BASE_URL}/api/randomquestion`)
//         .then(function (response) {
//             // 设置题目
//             document.getElementById('question').innerText = response.data.q_stem;
//             this.id = response.data.id;
//             // 清空选项区域
//             const optionsContainer = document.getElementById('options');
//             optionsContainer.innerHTML = ''; // 清空现有选项

//             const options = response.data.options;
//             const splitData = options.split('|');

//             if (splitData.length === 2 && splitData.includes("正确") && splitData.includes("错误")) {
//                 // 如果选项是“正确|错误”格式
//                 createOption(optionsContainer, "A", "正确");
//                 createOption(optionsContainer, "B", "错误");
//             } else {
//                 // 创建一个对象来存储切分后的数据
//                 const alloptions = {};
//                 splitData.forEach(item => {
//                     const [key, value] = item.split("、"); // 根据冒号切分键值对
//                     alloptions[key] = value; // 将数据存储到对象中
//                 });

//                 // 动态生成选项
//                 createOption(optionsContainer, "A", alloptions["A"] || "无数据");
//                 createOption(optionsContainer, "B", alloptions["B"] || "无数据");
//                 createOption(optionsContainer, "C", alloptions["C"] || "无数据");
//                 createOption(optionsContainer, "D", alloptions["D"] || "无数据");
//             }
//         })
//         .catch(function (err) {
//             console.log(err);
//         });
// }

// // 动态创建选项的函数
// function createOption(container, optionKey, optionValue) {
//     const optionDiv = document.createElement('div');
//     optionDiv.className = 'option-item';
//     optionDiv.textContent = `${optionKey}、${optionValue}`;
//     container.appendChild(optionDiv);
// }

// // 获取随机题目接口2
// function fetchRandomQuestionA() {
//     axios.get(`${BASE_URL}/api/randomquestion`)
//         .then(function (response) {
//             // 设置题目
//             document.getElementById('questionA').innerText = response.data.q_stem;
//             this.idA = response.data.id;
//             // 清空选项区域
//             const optionsContainer = document.getElementById('optionsA');
//             optionsContainer.innerHTML = ''; // 清空现有选项

//             const options = response.data.options;
//             const splitData = options.split('|');

//             if (splitData.length === 2 && splitData.includes("正确") && splitData.includes("错误")) {
//                 // 如果选项是“正确|错误”格式
//                 createOption(optionsContainer, "A", "正确");
//                 createOption(optionsContainer, "B", "错误");
//             } else {
//                 // 创建一个对象来存储切分后的数据
//                 const alloptions = {};
//                 splitData.forEach(item => {
//                     const [key, value] = item.split("、"); // 根据冒号切分键值对
//                     alloptions[key] = value; // 将数据存储到对象中
//                 });

//                 // 动态生成选项
//                 createOption(optionsContainer, "A", alloptions["A"] || "无数据");
//                 createOption(optionsContainer, "B", alloptions["B"] || "无数据");
//                 createOption(optionsContainer, "C", alloptions["C"] || "无数据");
//                 createOption(optionsContainer, "D", alloptions["D"] || "无数据");
//             }
//         })
//         .catch(function (err) {
//             console.log(err);
//         });
// }

// // 获取相似题目的函数
// function fetchWrongQuestions() {
//     document.getElementById('question-display').style.display = 'block';
//     document.getElementById('text-display').style.display = 'none';
//     document.getElementById('analysis-container').style.display = 'none';
//     const questionDisplay = document.getElementById('question-display');
//     axios.get(`${wzyc}/api/question/${this.id}/similar`)
//         .then(function (response) {
//             console.log(response.data);
//             // 清空问题容器
//             questionDisplay.innerHTML = '';
//             // 遍历返回的数据并渲染到页面
//             response.data.forEach(item => {
//                 const questionDiv = document.createElement('div');
//                 questionDiv.className = 'question-container';
//                 // 添加问题文本
//                 const questionText = document.createElement('div');
//                 questionText.className = 'question';
//                 questionText.textContent = item.question;
//                 questionDiv.appendChild(questionText);

//                 // 添加选项（如果有）
//                 if (item.options) {
//                     const optionsDiv = document.createElement('div');
//                     optionsDiv.className = 'options';
//                     optionsDiv.style.display = 'block'; // 初始隐藏选项
//                     const options = item.options.split('|');
//                     options.forEach(option => {
//                         const optionText = document.createElement('div');
//                         optionText.textContent = option;
//                         optionsDiv.appendChild(optionText);
//                     });
//                     questionDiv.appendChild(optionsDiv);

//                     // 添加点击事件，点击题目时切换选项的显示状态
//                     // questionText.addEventListener('click', function () {
//                     //     if (optionsDiv.style.display === 'none') {
//                     //         optionsDiv.style.display = 'block';
//                     //     } else {
//                     //         optionsDiv.style.display = 'none';
//                     //     }
//                     // });
//                 }

//                 // 将问题添加到页面
//                 questionDisplay.appendChild(questionDiv);
//             });
//         })
//         .catch(function (err) {
//             console.log(err);
//             // 如果请求失败，显示错误信息
//             questionDisplay.innerHTML = '<div class="error">加载失败，请稍后重试。</div>';
//         });
// }

// // 实现按钮被点击后保持黑色
// // 获取所有具有 'btn-primary' 类的按钮
// document.querySelectorAll('.btn-primary').forEach(button => {
//     // 为每个按钮添加点击事件监听器
//     button.addEventListener('click', function () {
//         // 切换当前按钮的 'clicked' 类
//         this.classList.toggle('clicked');
//     });
// });


// // 获取法条推荐的函数
// function fetchTextContent() {
//     document.getElementById('question-display').style.display = 'none';
//     document.getElementById('text-display').style.display = 'block';
//     document.getElementById('analysis-container').style.display = 'none';
//     const textDisplay = document.getElementById('text-display');
//     // 发送Axios请求获取法条分析内容
//     axios.get(`${BASE_URL}/api/lows?questionid=${this.id}`)
//         .then(function (response) {
//             // console.log(response.data)

//             // 清空法条容器
//             textDisplay.innerHTML = '';
//             // 遍历返回的数据并渲染到页面
//             response.data.forEach(item => {
//                 const textDiv = document.createElement('div');
//                 textDiv.className = 'text-container';
//                 // 添加法条文本
//                 const textText = document.createElement('div');
//                 textText.className = 'text';
//                 textText.innerHTML = item.law_name + '<br>' + item.chapter + '<br>' + item.article_content;
//                 textDiv.appendChild(textText);

//                 // 将法条添加到页面
//                 textDisplay.appendChild(textDiv);
//                 // console.log(12)
//             });
//         }).catch(function (err) {
//             console.log(err)
//         });
// }

// // 获取法理分析的函数
// function fetchLegalAnalysis() {
//     document.getElementById('question-display').style.display = 'none';
//     document.getElementById('text-display').style.display = 'none';
//     document.getElementById('analysis-container').style.display = 'block';
//     // 发送Axios请求获取法理分析内容
//     if (this.id != null) {
//         axios.get(`${BASE_URL}/api/analysis?questionid=${this.id}`)
//             .then(function (response) {
//                 const analysisData = JSON.parse(response.data.analysis);
//                 const analysisText = analysisData.Analysis || analysisData.Answer;
//                 displayTypingEffect(analysisText);
//             }).catch(function (err) {
//                 console.log(err);
//             });

//     }
// }

// // 打字机效果函数
// function displayTypingEffect(text) {
//     const analysisContainer = document.getElementById('analysis-container');
//     analysisContainer.innerHTML = ''; // 清空容器内容
//     let index = 0;

//     function type() {
//         if (index < text.length) {
//             analysisContainer.innerHTML += text.charAt(index);
//             index++;
//             setTimeout(type, 10); // 设置打字速度
//         }
//     }

//     type();
// }

// 语音助手的开始页面初始化的三条信息
function selectMessage(message) {
    document.getElementById('chat-input').innerHTML = message;
}

// 语音助手的开始页面初始化的三条信息
function selectMessage_test(message) {
    const qaMessages = document.getElementById("qa_messages");
    qaMessages.classList.remove("show");

    const dataMessages = document.getElementById("data_messages");
    dataMessages.classList.remove("show");

    document.getElementById('chat-input').innerHTML = message;
}

// 获取chat_id的接口
function getChatId() {

    this.user_id = getRandomIdFromCookie(); // 从 cookie 获取用户 ID
    const randomId = getRandomIdFromCookie();

    axios.get(`${BASE_URL}/api/chat_id_title_list?user_id=${randomId}`)
        .then(function (response) {
            let historyIds = response.data.chat_id_list;
            console.log('historyIds.length', historyIds)
            // 如果没有历史记录，分配新的 chat_id
            if (historyIds.length === 0) {
                axios.get(`${BASE_URL}/api/chatid?user_id=${this.user_id}`)
                    .then(function (response) {
                        // 获取 chat_id
                        this.chat_id = response.data.chat_id;
                        // localStorage.setItem('chat_id', this.chat_id);
                        console.log('没有历史记录，分配新的 chat_id:', this.chat_id);
                    })
                    .catch(function (err) {
                        console.log(err);
                    });
            } else {
                // 获取索引为 0 的历史记录
                const firstHistory = historyIds[0];
                // 如果历史记录有 title，重新获取 chat_id
                if (firstHistory.title) {
                    axios.get(`${BASE_URL}/api/chatid?user_id=${this.user_id}`)
                        .then(function (response) {
                            // 获取 chat_id
                            this.chat_id = response.data.chat_id;
                            // localStorage.setItem('chat_id', this.chat_id);
                            console.log('历史记录有 title，重新获取 chat_id:', this.chat_id);
                        })
                        .catch(function (err) {
                            console.log(err);
                        });
                } else {
                    this.chat_id = firstHistory.chat_id
                }
            }
        })
        .catch(function (err) {
            console.log(err);
        });
}

// 学习对话接口
async function sendMessage() {
    const input = document.getElementById('chat-input');
    const messageText = input.innerHTML;
    // const rendermessage = this.md.render(messageText);
    console.log(messageText)
    if (messageText) {
        // 添加用户消息
        const userMessage = document.createElement('div');
        userMessage.className = 'message user-message';
        userMessage.innerHTML = `
            <div class="message-content">
                <div class="message-text" style="color:white">${messageText}</div>
            </div>
            <img src="images/user.png" alt="User Avatar" class="avatar">
        `;
        document.getElementById('chat-messages').appendChild(userMessage);
        // 清空输入框
        input.innerHTML = '';
        try {
            // 发送POST请求
            const response = await fetch(`${BASE_URL}/api/chat/train`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ user_input: messageText, if_kb: this.if_kb, question_id: this.idA, chat_id: "f47e82a1-1878-453f-81e9-e9641773abd6" })
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let accumulatedMessage = ''; // 用于存储累积的消息
            // 创建机器人消息容器
            const botMessage = document.createElement('div');
            botMessage.className = 'message bot-message';
            const uniqueId = `audio-${Date.now()}`;
            botMessage.innerHTML = `
                <img src="images/robot.png" alt="Bot Avatar" class="avatar">
                <div class="message-content" style="background-color: #e5e5e5;">
                    <div class="message-text">${accumulatedMessage}</div>
                    <i class="fa-regular fa-circle-play" id="play_${uniqueId}" style="display:none;" onclick="bf_vedio('${uniqueId}', '${accumulatedMessage}')"></i>
                    <i class="fa-regular fa-circle-pause" style="display:none" id="pause_${uniqueId}" onclick="zt_vedio('${uniqueId}')"></i>
                    <audio id="${uniqueId}" style="display:none"></audio>
                </div>
            `;
            document.getElementById('chat-messages').appendChild(botMessage);
            // 获取消息文本容器
            const messageTextContainer = botMessage.querySelector('.message-text');
            const playButton = botMessage.querySelector(`#play_${uniqueId}`);
            const pauseButton = botMessage.querySelector(`#pause_${uniqueId}`);
            async function read() {
                const { done, value } = await reader.read();
                if (done) {
                    // 显示播放按钮
                    playButton.style.display = 'block';
                    return;
                }
                const responseText = decoder.decode(value);
                // 解析SSE格式的数据
                const lines = responseText.split('\n');
                console.log(lines)
                for (let i = 0; i < lines.length; i++) {
                    const line = lines[i].trim();
                    if (line.startsWith('event:update')) {
                        // 找到对应的data行
                        const dataLine = lines[i + 1]?.trim();
                        if (dataLine && dataLine.startsWith('data:')) {
                            const data = dataLine.slice(5).trim();
                            if (data) {
                                // 累积AI消息
                                accumulatedMessage += data;
                                // 使用 marked.js 将 Markdown 转换为 HTML
                                const htmlContent = this.md.render(accumulatedMessage);
                                // 更新机器人消息内容
                                // setTimeout(() => {
                                messageTextContainer.innerHTML = htmlContent;
                                playButton.setAttribute('onclick', `bf_vedio('${uniqueId}', '${accumulatedMessage}')`);
                                // }, 200);
                                // 滚动到底部
                                const chatMessages = document.getElementById('chat-messages');
                                chatMessages.scrollTop = chatMessages.scrollHeight;
                            }
                        }
                    }
                }
                await read();
            }
            await read();
        } catch (error) {
            console.error('Fetch failed:', error);
        }
    }
}

let streamingInProgress = false;
let currentMarkdown = ""; // 保存 Markdown 格式内容

// TODO :  chat_id暂时未改好  20250206
// step3不能渲染markdown格式
async function sendMessagedemo() {
    const input = document.getElementById('chat-input');
    const messageText = input.innerHTML;
    if (messageText) {
        // 添加用户消息
        const userMessage = document.createElement('div');
        userMessage.className = 'message user-message';
        userMessage.innerHTML = `
            <div class="message-content">
                <div class="message-text">${messageText}</div>
            </div>
            <img src="images/user.png" alt="User Avatar" class="avatar">
        `;
        document.getElementById('chat-messages').appendChild(userMessage);
        // 清空输入框
        input.innerHTML = '';
        if (streamingInProgress) return;
        streamingInProgress = true;
        try {
            // 发送 POST 请求
            const response = await fetch("https://nlp-demo.szmckj.cn/api/chat/analysis", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    user_input: messageText,
                    chat_id: "f47e82a1-1878-453f-81e9-e9641773abd6",
                    database_id: "string",
                }),
            });
            if (!response.ok) {
                throw new Error(`HTTP error: ${response.status}`);
            }

            // 初始化 dataContent 和 step8Content
            let dataContent = '';
            let step8Content = '';
            let isStep8Active = false;
            const step8Div = document.getElementById('step8');

            // 创建 bot 消息容器
            const botMessage = document.createElement('div');
            botMessage.className = 'message bot-message';
            const uniqueId = `audio-${Date.now()}`;
            botMessage.innerHTML = `
                <img src="images/robot.png" alt="Bot Avatar" class="avatar">
                <div class="message-content">
                    <div class="message-text">
                        <div class="loading-indicator">正在生成...</div>
                    </div>
                    <i class="fa-regular fa-circle-play" id="play_${uniqueId}" style="display:none;" onclick="bf_vedio('${uniqueId}', '${dataContent}')"></i>
                    <i class="fa-regular fa-circle-pause" style="display:none" id="pause_${uniqueId}" onclick="zt_vedio('${uniqueId}')"></i>
                    <audio id="${uniqueId}" style="display:none"></audio>
                </div>
            `;
            document.getElementById('chat-messages').appendChild(botMessage);

            // 获取消息文本容器
            const contentDiv = botMessage.querySelector('.message-text');

            // 初始化 Markdown 渲染器
            const md = window.markdownit({
                html: true,
                linkify: true,
                typographer: true,
            }).use(window.markdownitTaskLists, {
                enabled: true,
                label: true,
                labelAfter: true,
            });

            const reader = response.body.getReader();
            const decoder = new TextDecoder("utf-8");
            let buffer = '';
            let currentMarkdown = '';
            let lastEventType = null;

            // 修改后的内容更新函数
            function updateContent(newMarkdown, isHeader = false) {
                // 处理分隔符逻辑
                if (isHeader) {
                    if (lastEventType !== 'header') {
                        currentMarkdown += `\n\n---\n\n`;
                    }
                    currentMarkdown += `### ${newMarkdown}\n\n`;
                    lastEventType = 'header';
                } else {
                    if (currentMarkdown.includes('正在生成...')) {
                        currentMarkdown = '';
                    }
                    currentMarkdown += newMarkdown;
                    lastEventType = 'content';
                }
                contentDiv.innerHTML = md.render(currentMarkdown);
            }

            // 修改后的 processSSEChunk 函数
            function processSSEChunk(chunk) {
                const lines = chunk.split(/(?<=\n)/);
                let currentEvent = null;
                for (let line of lines) {
                    line = line.trim();
                    if (!line) continue;
                    if (line.startsWith("event:")) {
                        currentEvent = line.slice(6).trim();
                        if (currentEvent === "step8") {
                            isStep8Active = true;
                        }
                    } else if (line.startsWith("data:")) {
                        const content = line.slice(5).trim();
                        if (!content) continue;

                        // 更新 step8Div 和机器人消息内容的逻辑
                        if (isStep8Active && currentEvent === "update") {
                            step8Content += content;
                            if (step8Div) {
                                step8Div.classList.remove('has-content');
                                step8Div.innerHTML = step8Content;
                            }
                            dataContent += content;
                            updateContent(dataContent);
                            dataContent = '';
                        } else if (currentEvent?.startsWith('step')) {
                            const stepNumber = currentEvent.replace('step', '');
                            const stepTitle = `Step ${stepNumber}: ${content}`;
                            updateContent(stepTitle, true);
                        } else if (currentEvent === "update") {
                            dataContent += content;
                            if (content.endsWith('.') || content.endsWith('。') || dataContent.length > 50) {
                                updateContent(dataContent);
                                dataContent = '';
                            }
                        } else if (currentEvent === "sqldata") {
                            // 处理 sqldata 事件
                            this.echartsData = content; // 假设数据是 JSON 格式
                            console.log('echartsData:', this.echartsData);
                            // 创建 CustomEvent 对象
                            const event = new CustomEvent('sqldataReceived', {
                                detail: this.echartsData // 将数据作为 detail 传递
                            });

                            // 触发事件
                            window.dispatchEvent(event);
                            // 这里可以根据需要将 echartsData 传递给 ECharts 进行渲染
                        }
                    }
                }
                if (dataContent.length > 0) {
                    updateContent(dataContent);
                    dataContent = '';
                }
            }

            async function read() {
                while (true) {
                    const { done, value } = await reader.read();
                    if (done) {
                        streamingInProgress = false;
                        isStep8Active = false;
                        return;
                    }
                    buffer += decoder.decode(value, { stream: true });
                    let boundary;
                    while ((boundary = buffer.indexOf('\n\n')) !== -1) {
                        const chunk = buffer.slice(0, boundary);
                        buffer = buffer.slice(boundary + 2);
                        processSSEChunk(chunk);
                    }
                    const chatMessages = document.getElementById('chat-messages');
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                }
            }
            await read();
        } catch (error) {
            console.error("Error during SSE POST request:", error);
            streamingInProgress = false;
            const errorDiv = document.createElement('div');
            errorDiv.className = 'message-error';
            errorDiv.textContent = '消息发送失败，请重试';
            document.getElementById('chat-messages').appendChild(errorDiv);
        }
    }
}

// 是否开启知识库搜素
function handleCheckboxChange(checkbox) {
    if (checkbox.checked) {
        this.if_kb = true;
    } else {
        this.if_kb = false;
    }
}

// 播放语音
function bf_vedio(audioId, text) {
    const playButton = document.getElementById(`play_${audioId}`);
    const pauseButton = document.getElementById(`pause_${audioId}`);
    const audioElement = document.getElementById(audioId);

    // 检查是否有音频在播放，如果有则先暂停
    if (!audioElement.paused) {
        audioElement.pause();
        playButton.style.display = 'block';
        pauseButton.style.display = 'none';
        return;
    }

    // 如果音频已经加载过，且当前处于暂停状态，则从暂停位置继续播放
    if (audioElement.src && audioElement.paused) {
        playButton.style.display = 'none';
        pauseButton.style.display = 'block';
        audioElement.play();
        return;
    }

    // 如果音频未加载过，则请求新的音频数据
    playButton.style.display = 'none';
    pauseButton.style.display = 'block';

    axios.post(`${BASE_URL}/api/tts`, { tts_text: text }, { responseType: 'blob' })
        .then(function (response) {
            const blob = new Blob([response.data], { type: 'audio/mpeg' }); // 确保类型正确
            const url = URL.createObjectURL(blob);
            audioElement.src = url;

            // 监听音频播放结束事件
            audioElement.onended = function () {
                playButton.style.display = 'block';
                pauseButton.style.display = 'none';
            };

            // 播放音频
            audioElement.play();
        })
        .catch(function (err) {
            console.log(err);
        });
}

// 暂停语音
function zt_vedio(audioId) {
    const playButton = document.getElementById(`play_${audioId}`);
    const pauseButton = document.getElementById(`pause_${audioId}`);
    const audioElement = document.getElementById(audioId);

    if (audioElement && !audioElement.paused) {
        audioElement.pause();
        playButton.style.display = 'block';
        pauseButton.style.display = 'none';
    }
}

// 随机生成示例
const tech_ai_texts = [
    "人工智能的快速发展正在改变我们的生活方式。",
    "大数据与机器学习为精准医疗提供了新的可能性。",
    "自动驾驶技术正在不断提升出行的安全性和便利性。",
    "云计算让企业能够更加高效地管理和存储数据。",
    "量子计算有望解决传统计算机无法处理的复杂问题。"
]
const weather_daily_texts = [
    "今天的天气晴朗，非常适合外出运动和休闲活动。",
    "未来几天可能有小雨，请记得随身携带雨具。",
    "寒冷的冬季里，及时添加衣物以免着凉。",
    "春天的清晨常伴有微风，带来一丝凉意。",
    "夏日的午后，骄阳似火，需要做好防晒措施。"
]

function displayRandomTexts() {
    // 随机选择tech_ai_texts中的一条文本
    const randomTechText = tech_ai_texts[Math.floor(Math.random() * tech_ai_texts.length)];
    console.log(randomTechText)

    // 随机选择weather_daily_texts中的一条文本
    const randomWeatherText = weather_daily_texts[Math.floor(Math.random() * weather_daily_texts.length)];
    console.log(randomWeatherText)

    // 将随机选择的文本显示在id为AI_text和user_text的元素中
    document.getElementById('AI_text').textContent = randomTechText;
    document.getElementById('user_text').textContent = randomWeatherText;
}

let historyData = [];
// 历史记录
// 当点击历史记录图标时，显示弹框
function loadHistory() {
    // 获取历史记录按钮
    const historyButton = document.getElementById("history");
    historyButton.addEventListener("click", function (event) {
        // 阻止点击事件传播到 document 上
        event.stopPropagation();

        // 显示历史记录模态框
        const historyModal = document.getElementById("historyModal");
        historyModal.classList.add("active");

        // 获取cookie中的随机ID
        const randomId = getRandomIdFromCookie();

        // 调用 API 获取历史记录
        axios.get(`${BASE_URL}/api/chat_id_title_list?user_id=${randomId}`)
            .then(function (response) {
                let historyIds = response.data.chat_id_list;
                // 过滤掉索引为 0 的元素
                historyIds = historyIds.slice(1);

                // 获取 ul 元素
                const historyList = document.getElementById("historyList");
                historyList.innerHTML = '';  // 清空现有的历史记录列表

                // 遍历数组，为每个 id 创建一个 li 元素，并添加点击事件
                historyIds.forEach(item => {
                    // 只有当 item.title 存在时才创建 li 元素
                    if (!item.title) return;

                    const li = document.createElement("li");
                    li.textContent = item.title;

                    // 添加点击事件，点击时打印 chat_id，并传递 chat_id 发起请求
                    li.addEventListener("click", function () {
                        // 关闭历史记录模态框
                        historyModal.classList.remove("active");

                        // 调用 API 获取指定 chat_id 的聊天记录
                        axios.get(`${BASE_URL}/api/chat_byid?chat_id=${item.chat_id}`)
                            .then(function (response) {
                                // console.log(response.data.messages.history);

                                this.chat_id = item.chat_id;
                                console.log('this.chat_id',this.chat_id);

                                // 清空全局的 historyData 数组，防止数据累加
                                historyData = [];

                                // 重新获取新的历史记录数据并存入 historyData
                                const newHistory = (response.data.messages && response.data.messages.history) || [];
                                historyData.push(...newHistory);

                                // 清空聊天记录显示区域，防止重复渲染相同的消息
                                const chatMessagesContainer = document.getElementById('chat-messages');
                                chatMessagesContainer.innerHTML = '';

                                // 渲染历史记录
                                historyData.forEach(msg => {
                                    const msgContainer = document.createElement('div');
                                    msgContainer.className = `message ${msg.role === 'user' ? 'user-message' : 'bot-message'}`;
                                    msgContainer.innerHTML = `
                                        <img src="${msg.role === 'user' ? 'images/user.png' : 'images/robot.png'}" alt="${msg.role} Avatar" class="avatar">
                                        <div class="message-content">
                                            <div class="message-text">${msg.content}</div>
                                        </div>
                                    `;
                                    chatMessagesContainer.appendChild(msgContainer);
                                });

                                // 滚动到聊天记录的底部
                                chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
                            }).catch(function (err) {
                                console.log(err);
                            });
                    });

                    // 将 li 元素添加到历史记录列表
                    historyList.appendChild(li);
                });
            }).catch(function (err) {
                console.log(err);
            });
    });
}

// 生成一个随机的ID
function generateRandomId() {
    return 'LG_id_' + Math.random().toString(36).substr(2, 8); // 生成一个8位的随机ID
}

// 存储随机 ID 到 Cookie 中
function setRandomIdInCookie() {
    // 判断是否存在id
    const existingId = getRandomIdFromCookie();
    if (existingId) {
        console.log(`Cookie中已存在随机ID: ${existingId}`);
        return; // 如果已经存在则不再设置
    }

    const randomId = generateRandomId();
    // 设置过期时间为 2099 年 12 月 31 日 23:59:59 GMT
    const expires = "Fri, 31 Dec 2099 23:59:59 GMT";

    // 设置 id，包含随机 ID 和过期时间
    document.cookie = `LG_Id=${randomId}; expires=${expires}; path=/`;
    console.log(`Random ID stored in cookie: ${randomId}`);
}

// 获取 cookie中设置的 随机 ID
function getRandomIdFromCookie() {
    const cookieArray = document.cookie.split('; ');
    for (let i = 0; i < cookieArray.length; i++) {
        const cookie = cookievalue = cookieArray[i].split('=');
        if (cookie[0] === 'LG_Id') {
            return cookie[1];
        }
    }
    return null; // 如果没有随机 ID，返回 null
}


// 需要初始化的api
window.onload = function () {
    // 创建 markdown-it 实例并注册 task-lists 插件
    this.md = window
        .markdownit({
            html: true,
            linkify: true,
            typographer: true,
        })
        .use(window.markdownitTaskLists, {
            enabled: true,
            label: true,
            labelAfter: true,
        });
    setRandomIdInCookie();
    getChatId()
    // fetchRandomQuestion();
    // TestfetchRandomQuestion()
    // fetchRandomQuestionA();
    // setTimeout(() => {
    //     fetchLegalAnalysis();
    // }, 1000);

    displayRandomTexts();
}