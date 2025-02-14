const BASE_URL = '';

const md = null;

const chartContainer = document.getElementById('chart-container');
const myChart = echarts.init(chartContainer);

const barchartData = {
    grid: {
        top: '10%',    // 上边距
        bottom: '10%', // 下边距
        left: '10%',   // 左边距
        right: '10%'   // 右边距
    },
    tooltip: {
        trigger: 'axis', // 按坐标轴触发
        formatter: function (params) {
            // 自定义提示框内容
            let result = `名称：${params[0].name}<br>`; // 显示 x 轴名称
            params.forEach(param => {
                result += `值：${param.value}<br>`; // 显示系列名称和数据值
            });
            return result;
        }
    },
    xAxis: {
        type: 'category',
        data: [],
        axisLabel: {
            formatter: function (value) {
                if (value.length > 6) {
                    return value.substring(0, 6) + '...'; // 超过 3 个字符，显示省略号
                }
                return value;
            }
        }
    },
    yAxis: {
        type: 'value'
    },
    series: [
        {
            data: [],
            type: 'bar'
        }
    ]
};

// const piechartData = {
//     grid: {
//         top: '10%',    // 上边距
//         bottom: '10%', // 下边距
//         left: '10%',   // 左边距
//         right: '10%'   // 右边距
//     },
//     // tooltip: {
//     //     trigger: 'item', // 按数据项触发
//     //     formatter: function (params) {
//     //         return `${params.name}: ${params.value} (${(params.percent).toFixed(2)}%)`;
//     //     }
//     // },
//     tooltip: {
//         trigger: 'item'
//     },
//     series: [
//         {
//             type: 'pie',
//             radius: '50%',
//             data: [
//             ]
//         }
//     ]
// };

// const linechartData = {
//     grid: {
//         top: '10%',    // 上边距
//         bottom: '10%', // 下边距
//         left: '10%',   // 左边距
//         right: '10%'   // 右边距
//     },
//     tooltip: {
//         trigger: 'axis', // 按坐标轴触发
//         formatter: function (params) {
//             // 自定义提示框内容
//             let result = `名称：${params[0].name}<br>`; // 显示 x 轴名称
//             params.forEach(param => {
//                 result += `值：${param.value}<br>`; // 显示系列名称和数据值
//             });
//             return result;
//         }
//     },
//     xAxis: {
//         type: 'category',
//         data: [],
//         axisLabel: {
//             formatter: function (value) {
//                 if (value.length > 6) {
//                     return value.substring(0, 6) + '...'; // 超过 3 个字符，显示省略号
//                 }
//                 return value;
//             }
//         }
//     },
//     yAxis: {
//         type: 'value'
//     },
//     series: [
//         {
//             data: [],
//             type: 'line'
//         }
//     ]
// };

// 动态转换数据
function transformData(jsonData, type) {
    if (type === 'bar') {
        return {
            grid: {
                top: '10%',    // 上边距
                bottom: '10%', // 下边距
                left: '10%',   // 左边距
                right: '10%'   // 右边距
            },
            tooltip: {
                trigger: 'axis', // 按坐标轴触发
                formatter: function (params) {
                    // 自定义提示框内容
                    let result = `名称：${params[0].name}<br>`; // 显示 x 轴名称
                    params.forEach(param => {
                        result += `值：${param.value}<br>`; // 显示系列名称和数据值
                    });
                    return result;
                }
            },
            xAxis: {
                type: 'category',
                data: jsonData.categories,
                axisLabel: {
                    formatter: function (value) {
                        if (value.length > 6) {
                            return value.substring(0, 6) + '...'; // 超过 3 个字符，显示省略号
                        }
                        return value;
                    }
                }
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    data: jsonData.values,
                    type: 'bar'
                }
            ]
        };
    }
    // else if (type === 'pie') {
    //     return {
    //         grid: {
    //             top: '10%',    // 上边距
    //             bottom: '10%', // 下边距
    //             left: '10%',   // 左边距
    //             right: '10%'   // 右边距
    //         },
    //         tooltip: {
    //             trigger: 'item'
    //         },
    //         series: [
    //             {
    //                 // name: '访问来源',
    //                 type: 'pie',
    //                 radius: '50%',
    //                 data: jsonData.pieData
    //             }
    //         ]
    //     };
    // } else if (type === 'line') {
    //     return {
    //         grid: {
    //             top: '10%',    // 上边距
    //             bottom: '10%', // 下边距
    //             left: '10%',   // 左边距
    //             right: '10%'   // 右边距
    //         },
    //         tooltip: {
    //             trigger: 'axis', // 按坐标轴触发
    //             formatter: function (params) {
    //                 // 自定义提示框内容
    //                 let result = `名称：${params[0].name}<br>`; // 显示 x 轴名称
    //                 params.forEach(param => {
    //                     result += `值：${param.value}<br>`; // 显示系列名称和数据值
    //                 });
    //                 return result;
    //             }
    //         },
    //         xAxis: {
    //             type: 'category',
    //             data: jsonData.categories,
    //             axisLabel: {
    //                 formatter: function (value) {
    //                     if (value.length > 6) {
    //                         return value.substring(0, 6) + '...'; // 超过 3 个字符，显示省略号
    //                     }
    //                     return value;
    //                 }
    //             }
    //         },
    //         yAxis: {
    //             type: 'value'
    //         },
    //         series: [
    //             {
    //                 data: jsonData.values,
    //                 type: 'line'
    //             }
    //         ]
    //     };
    // }
    return null;
}

myChart.setOption(barchartData, { notMerge: true });

// 假设从后端返回的 JSON 数据
const jsonData = {
    categories: [],
    // values: [],
    // pieData: [
    // ]
};
// 监听自定义事件
window.addEventListener('sqldataReceived', (event) => {
    const test = event.detail.replace(/'/g, '"');
    const test2 = JSON.parse(test)
    jsonData.categories = test2.categories; // 更新 categories
    jsonData.values = test2.values; // 更新 values
    // 将 categories 和 values 组合成 pieData
    const newPieData = jsonData.categories.map((category, index) => ({
        name: category,
        value: jsonData.values[index]
    }));

    // 更新 jsonData 的 pieData
    jsonData.pieData = newPieData;
    // 假设当前图表类型是 'bar'，你可以根据实际情况调整
    const chartData = transformData(jsonData, 'bar');

    if (chartData) {
        myChart.setOption(chartData, { notMerge: true });
    }
});

// 监听窗口大小变化，调整图表大小
window.addEventListener('resize', () => {
    myChart.resize();
});

// function switchChart(type) {
//     const chartData = transformData(jsonData, type);
//     if (chartData) {
//         myChart.setOption(chartData, { notMerge: true });
//         document.querySelectorAll('.chart-button').forEach(button => {
//             button.classList.remove('active');
//         });
//         document.getElementById(`${type}-chart-btn`).classList.add('active');
//     }
// }

// 切换面板的函数
function switchPanel(panelType, showAlert = true) {
    // 获取两个面板
    const qaPanel = document.getElementById('qa-panel');
    const dataPanel = document.getElementById('data-panel');
    const knowledgePanel = document.getElementById('knowledge-panel');

    // 移除所有面板的 active 类
    qaPanel.classList.remove('active');
    dataPanel.classList.remove('active');
    knowledgePanel.classList.remove('active');
    qaPanel.classList.remove('knowledge');
    dataPanel.classList.remove('knowledge');
    knowledgePanel.classList.remove('knowledge');
    qaPanel.classList.remove('active_data');
    dataPanel.classList.remove('active_data');
    knowledgePanel.classList.remove('active_data');


    // 根据点击的面板类型添加 active 类
    if (panelType === 'qa') {
        qaPanel.classList.add('active');
        if (showAlert) {
            document.getElementById('send-button_QA').style.display = 'block';
            document.getElementById('send-button').style.display = 'none';
            document.getElementById('qa_messages').style.display = 'block';

            document.getElementById('data_messages').style.display = 'none';
            document.getElementById('qa-button').style.display = 'block';
            document.getElementById('data-button').style.display = 'none';

            document.getElementById('knowledge_data_messages').style.display = 'none';
            document.getElementById('Q-data-button').style.display = 'none';
            document.getElementById('send-button-knowledge').style.display = 'none';
            const recordButton = document.getElementById('record_button');
            recordButton.style.backgroundColor = '#1FDE82';

            showMessage('已切换到 QA问答 模式');
        }
        // 这里可以添加 QA 问答相关的逻辑
    } else if (panelType === 'data') {
        dataPanel.classList.add('active_data');
        if (showAlert) {
            document.getElementById('send-button_QA').style.display = 'none';
            document.getElementById('send-button').style.display = 'block';
            document.getElementById('qa_messages').style.display = 'none';
            document.getElementById('data_messages').style.display = 'block';
            document.getElementById('qa-button').style.display = 'none';
            document.getElementById('data-button').style.display = 'block';
            document.getElementById('knowledge_data_messages').style.display = 'none';
            document.getElementById('Q-data-button').style.display = 'none';
            document.getElementById('send-button-knowledge').style.display = 'none';
            const recordButton = document.getElementById('record_button');
            recordButton.style.backgroundColor = '';
            showMessage('已切换到 问题提取 模式');
        }
    } else if (panelType === 'knowledge') {
        knowledgePanel.classList.add('knowledge');
        if (showAlert) {
            document.getElementById('knowledge_data_messages').style.display = 'block';
            document.getElementById('Q-data-button').style.display = 'block';
            document.getElementById('send-button-knowledge').style.display = 'block';
            document.getElementById('send-button_QA').style.display = 'none';
            document.getElementById('send-button').style.display = 'none';
            document.getElementById('qa_messages').style.display = 'none';
            document.getElementById('data_messages').style.display = 'none';
            document.getElementById('qa-button').style.display = 'none';
            document.getElementById('data-button').style.display = 'none';
            const recordButton = document.getElementById('record_button');
            const sendbutton = document.getElementById('send-button-knowledge');
            const Qbutton = document.getElementById('Q-data-button');
            Qbutton.style.backgroundColor = '#d5de2c';
            recordButton.style.backgroundColor = '#d5de2c';
            sendbutton.style.backgroundColor = '#d5de2c';
            showMessage('已切换到 知识整理 模式');
        }
    }
}

// 显示消息弹框的函数
function showMessage(message) {
    // 创建一个弹框元素
    const alertBox = document.createElement('div');
    alertBox.style.position = 'fixed';
    alertBox.style.top = '20px';
    alertBox.style.left = '50%';
    alertBox.style.transform = 'translateX(-50%)';
    alertBox.style.backgroundColor = 'rgba(76, 175, 80, 0.9)'; // 半透明的绿色背景
    alertBox.style.color = 'white';
    alertBox.style.padding = '12px 24px';
    alertBox.style.borderRadius = '8px';
    alertBox.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
    alertBox.style.zIndex = '1000';
    alertBox.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    alertBox.style.fontSize = '14px';
    alertBox.style.fontFamily = 'Arial, sans-serif';
    alertBox.style.textAlign = 'center';
    alertBox.style.cursor = 'pointer'; // 点击关闭
    alertBox.textContent = message;

    // 将弹框添加到页面中
    document.body.appendChild(alertBox);

    // 点击弹框关闭
    alertBox.addEventListener('click', () => {
        alertBox.style.opacity = '0';
        setTimeout(() => {
            document.body.removeChild(alertBox);
        }, 500); // 等待淡出动画完成
    });

    // 3 秒后淡出并移除弹框
    setTimeout(() => {
        alertBox.style.opacity = '0';
        setTimeout(() => {
            document.body.removeChild(alertBox);
        }, 500); // 等待淡出动画完成
    }, 800); // 3 秒后消失
}

// 默认选中 QA 问答区域，但不显示消息提示
switchPanel('qa', false); // 第二个参数为 false，表示不显示消息提示

// 获取 QA问答 Q 按钮和 qa_messages 元素
const qaButton = document.getElementById("qa-button");
const qaMessages = document.getElementById("qa_messages");

// 点击 Q 按钮时，显示/隐藏 qa_messages
qaButton.addEventListener("click", function (event) {
    // 阻止点击事件冒泡，避免触发 document 上的点击事件
    event.stopPropagation();
    qaMessages.classList.toggle("show");
});

// 阻止点击 qa_messages 内部内容时，事件冒泡到 document（避免误关闭弹框）
qaMessages.addEventListener("click", function (event) {
    event.stopPropagation();
});

// 点击页面其他区域时，隐藏 qa_messages
document.addEventListener("click", function (event) {
    // 如果点击的目标既不在 qa_messages 内，也不是 Q 按钮，则关闭 qa_messages
    if (!qaMessages.contains(event.target) && event.target !== qaButton) {
        qaMessages.classList.remove("show");
    }
});

// 获取 问题提取 Q 按钮和 data_messages 元素
const dataButton = document.getElementById("data-button");
const dataMessages = document.getElementById("data_messages");

// 点击 Q 按钮时，显示/隐藏 data_messages
dataButton.addEventListener("click", function (event) {
    // 阻止点击事件冒泡，避免触发 document 上的点击事件
    event.stopPropagation();
    dataMessages.classList.toggle("show");
});

// 阻止点击 data_messages 内部内容时，事件冒泡到 document（避免误关闭弹框）
dataMessages.addEventListener("click", function (event) {
    event.stopPropagation();
});

// 点击页面其他区域时，隐藏 data_messages
document.addEventListener("click", function (event) {
    // 如果点击的目标既不在 data_messages 内，也不是 Q 按钮，则关闭 data_messages
    if (!dataMessages.contains(event.target) && event.target !== qaButton) {
        dataMessages.classList.remove("show");
    }
});

// 获取 知识整理 Q 按钮和 knowledge_data_messages 元素
const knowledgeButton = document.getElementById("Q-data-button");
const knowledgeMessages = document.getElementById("knowledge_data_messages");

// 点击 Q 按钮时，显示/隐藏 knowledge_data_messages
knowledgeButton.addEventListener("click", function (event) {
    // 阻止点击事件冒泡，避免触发 document 上的点击事件
    event.stopPropagation();
    knowledgeMessages.classList.toggle("show");
});

// 阻止点击 knowledge_data_messages 内部内容时，事件冒泡到 document（避免误关闭弹框）
knowledgeMessages.addEventListener("click", function (event) {
    event.stopPropagation();
});

// 点击页面其他区域时，隐藏 knowledge_data_messages
document.addEventListener("click", function (event) {
    // 如果点击的目标既不在 knowledge_data_messages 内，也不是 Q 按钮，则关闭 knowledge_data_messages
    if (!knowledgeMessages.contains(event.target) && event.target !== qaButton) {
        knowledgeMessages.classList.remove("show");
    }
});

// 语音助手的开始页面初始化的三条信息
function selectMessage_test(message) {
    const qaMessages = document.getElementById("qa_messages");
    qaMessages.classList.remove("show");

    const dataMessages = document.getElementById("data_messages");
    dataMessages.classList.remove("show");

    const konwledgeMessages = document.getElementById("knowledge_data_messages");
    konwledgeMessages.classList.remove("show");

    document.getElementById('chat-input').innerHTML = message;
}

// // 当点击关闭按钮时，隐藏历史会话弹框
// document.getElementById("closeModal").addEventListener("click", function (event) {
//     // 阻止点击事件传播到 document 上
//     event.stopPropagation();
//     document.getElementById("historyModal").classList.remove("active");
// });

// // 当点击页面的其他区域时，关闭历史会话弹框
// document.addEventListener("click", function (event) {
//     const modal = document.getElementById("historyModal");
//     const historyButton = document.getElementById("history");

//     // 如果点击的区域不是弹框本身或历史记录按钮，则关闭弹框
//     if (!modal.contains(event.target) && event.target !== historyButton) {
//         modal.classList.remove("active");
//     }
// });

// 获取日期选择器和下拉菜单的DOM元素
const datePicker = document.getElementById('date-picker');
const dataPickerStop = document.getElementById('data-picker-stop');
const orderSelector = document.getElementById('order-selector');
const selectedDate = null;
const selectDateStop = null;
const selectedOrderTitle = null;
// 定义全局变量存储上一次的姓名ID和日期
let lastSelectedId = null;
let lastSelectedDate = null;
let lastSelectedDateStop = null;
let lastSelectedOrderTitle = null;

const selectedId = null;

// 获取开始日期值
function handletimeChange() {
    this.selectedDate = document.getElementById('date-picker').value;
    console.log('选择的开始日期:', this.selectedDate);
    checkAndTriggerGetOrderTag()
    checkAndTriggerGetOrderDetail()
}
// 获取结束日期值
function handlestoptimeChange() {
    this.selectDateStop = document.getElementById('date-picker-stop').value;
    console.log('选择的结束日期:', this.selectDateStop);
    checkAndTriggerGetOrderTag()
    checkAndTriggerGetOrderDetail()
}

//获取选中的姓名
function selectName(element) {
    // 获取选中的姓名和对应的ID
    this.selectedId = element.getAttribute('data-id');

    console.log('Associated ID:', this.selectedId);

    // 移除所有已选中的样式
    const selectedElements = document.querySelectorAll('.name-tag.selected');
    selectedElements.forEach(selectedElement => {
        selectedElement.classList.remove('selected');
    });

    // 添加选中样式到当前点击的元素
    element.classList.add('selected');
    checkAndTriggerGetOrderTag()
    checkAndTriggerGetOrderDetail()
}

// 获取所有 工单标签 Tab 按钮并为它们添加点击事件监听器
document.getElementById('order-selector').addEventListener('click', (event) => {
    const button = event.target.closest('.tab-button');
    if (button && button.value) {
        // 先移除所有按钮的激活状态
        document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active-tab'));
        // 为当前按钮添加激活状态
        button.classList.add('active-tab');
        // 从 value 属性中获取完整的 caseid
        const selectedTitle = button.value;
        // 更新全局变量
        this.selectedOrderTitle = selectedTitle;
        console.log('选择的工单标题:', selectedTitle);
        // 调用其他函数处理选中的标题
        checkAndTriggerGetOrderDetail();
    }
});

// 控制工单标签的滑动
function scrollTabs(direction) {
    const tabContainer = document.getElementById('order-selector');
    if (tabContainer) {
        const scrollAmount = 100; // 可根据实际情况调整滑动的距离
        if (direction === 'left') {
            tabContainer.scrollLeft -= scrollAmount;
        } else if (direction === 'right') {
            tabContainer.scrollLeft += scrollAmount;
        }
    }
}

// 切换AI评价
function switchAI() {
    console.log('切换AI评价');
    const AI_evaluation = document.getElementById('AI_evaluation');
    const Echarts = document.getElementById('echarts');
    AI_evaluation.style.display = 'none';
    Echarts.style.display = 'block';
}

// AI评价框中的四个按钮
let activeButton = null; // 用于记录当前激活的按钮
function handleButtonClick(button) {
    // 如果已经有激活的按钮，移除其激活样式
    if (activeButton) {
        activeButton.classList.remove('active');
    }

    // 为当前点击的按钮添加激活样式
    button.classList.add('active');
    activeButton = button; // 更新当前激活的按钮

    // 根据按钮的 ID 执行不同的操作
    if (button.id === 'show-evaluation') {
        fetchEvaluation();
    } else if (button.id === 'show-reply') {
        fetchsummery();
    } else if (button.id === 'show-knowledge') {
        fetchKnowledge();
    } else if (button.id === 'show-think') {
        fetchThink();
    }
}

// 切换echarts图表
function switchecharts() {
    console.log('切换echarts图表');
    const AI_evaluation = document.getElementById('AI_evaluation');
    const Echarts = document.getElementById('echarts');
    AI_evaluation.style.display = 'block';
    Echarts.style.display = 'none';
}

// 检查是否需要触发获取工单标签的函数
function checkAndTriggerGetOrderTag() {
    // 检查是否选中了姓名和日期
    if (this.selectedId && this.selectedDate && this.selectDateStop) {
        // 检查是否与上一次的值不一致
        if (this.selectedId !== this.lastSelectedId || this.selectedDate !== this.lastSelectedDate || this.selectDateStop !== this.lastSelectedDateStop) {
            getOrderTag();
            const AI_problemdescription = document.getElementById('AI_problemdescription');
            if (AI_problemdescription) {
                AI_problemdescription.style.display = "none";
                this.AI_problem_desc = null;
            }

            const kfreply = document.getElementById('AI_problemreply');
            if (kfreply) {
                kfreply.style.display = "none";
                this.AI_kf_Reply = null;
            }
            // 更新上一次的值
            this.lastSelectedId = this.selectedId;
            this.lastSelectedDate = this.selectedDate;
            this.lastSelectedDateStop = this.selectDateStop;
        }
    }
}

// 检查是否需要触发获取工单详情的函数
function checkAndTriggerGetOrderDetail() {
    // 检查是否选中了姓名、日期和工单标题
    if (this.selectedId && this.selectedDate && this.selectedOrderTitle && this.selectDateStop) {
        // 检查是否与上一次的值不一致
        if (this.selectedId !== this.lastSelectedId || this.selectedDate !== this.lastSelectedDate || this.selectedOrderTitle !== this.lastSelectedOrderTitle || this.selectDateStop !== this.lastSelectedDateStop) {
            console.log('触发获取工单详情接口');
            getOrderDetail();
            const AI_problemdescription = document.getElementById('AI_problemdescription');
            if (AI_problemdescription) {
                AI_problemdescription.style.display = "none";
                this.AI_problem_desc = null;
            }
            const kfreply = document.getElementById('AI_problemreply');
            if (kfreply) {
                kfreply.style.display = "none";
                this.AI_kf_Reply = null;
            }
            // 更新上一次的值
            this.lastSelectedId = this.selectedId;
            this.lastSelectedDate = this.selectedDate;
            this.lastSelectedOrderTitle = this.selectedOrderTitle;
            this.lastSelectedDateStop = this.selectDateStop;
        }
    }
}

// 获取工单标签
function getOrderTag() {
    // 使用axios调用接口获取工单标签
    axios.get(`${BASE_URL}/lg/caseids?creatby=${this.selectedId}&createtime_start=${this.selectedDate}&createtime_end=${this.selectDateStop}`)
        .then(function (response) {
            const orderSelector = document.getElementById('order-selector');
            orderSelector.innerHTML = ''; // 清空之前的选项
            const order_caseid = response.data;
            order_caseid.forEach(cid => {
                const option = document.createElement('div');
                option.className = 'tab-button';
                option.value = cid.caseid;
                option.textContent = cid.caseid.toString().slice(-4);
                orderSelector.appendChild(option);
            });
        })
        .catch(function (error) {
            console.error('获取工单标签失败:', error);
        });
}

let ai_comment = null;
let think = null;
let summer_reply = null;
let kf_reply = null;

// 获取think
function fetchThink() {
    const jsonContent = this.md.render(this.think);
    document.getElementById('response').innerHTML = jsonContent;
}

// 获取DS思考结果
function fetchEvaluation() {
    const jsonContent = this.md.render(this.ai_comment);
    // 提取 Response 部分的内容
    document.getElementById('response').innerHTML = jsonContent;

}

// 提取 JSON 字符串
function extractJsonFromMarkdown(markdown) {
    // 使用正则表达式匹配 ```json 和 ``` 之间的内容
    const regex = /```[\s]*json([\s\S]*?)```/;
    const match = markdown.match(regex);

    if (match && match[1]) {
        return match[1].trim(); // 返回去掉首尾空白的 JSON 字符串
    } else {
        console.warn('未找到有效的 JSON 内容');
        return null;
    }
}

// 获取客服回复得分标准
function fetchKnowledge() {
    if (this.kf_reply) {
        const filteredScore = this.kf_reply.replace(/[\s\S]*?<\/think>/, '')
        const jsonContent = this.md.render(filteredScore);

        document.getElementById('response').innerHTML = jsonContent;

        // 使用示例
        const jsonString = extractJsonFromMarkdown(filteredScore);

        // 解析 JSON 字符串
        try {
            const data = JSON.parse(jsonString);
            // console.log("解析后的数据:", data);
            if (data) {
                const finalScore = data.Response["最终得分"];
                // console.log("最终得分:", finalScore);
                document.getElementById('kf_score').textContent = finalScore;
            } else {
                // console.log('wu')
                document.getElementById('kf_score').textContent = "-";
            }

        } catch (error) {
            console.error("JSON解析错误:", error);
        }
    } else {
        document.getElementById('response').innerHTML = '暂无评分准则';
        document.getElementById('kf_score').textContent = "-";
    }
}

// 获取小结准确度得分标准
function fetchsummery() {
    if (this.summer_reply) {
        const filteredScore = this.summer_reply.replace(/[\s\S]*?<\/think>/, '')
        // console.log('filteredScore:', filteredScore);
        const jsonContent = this.md.render(filteredScore);

        document.getElementById('response').innerHTML = jsonContent;

        // 使用示例
        const jsonString = extractJsonFromMarkdown(filteredScore);

        console.log("JSON字符串:", jsonString);

        // 解析 JSON 字符串
        try {
            const data = JSON.parse(jsonString);
            // console.log("解析后的数据:", data);
            if (data) {
                const finalScore = data.Response["final_score"];
                document.getElementById('fit_score').textContent = finalScore;
            } else {
                // console.log('wu')
                document.getElementById('fit_score').textContent = "-";
            }

        } catch (error) {
            console.error("JSON解析错误:", error);
        }
    } else {
        document.getElementById('response').innerHTML = '暂无评分准则';
        document.getElementById('fit_score').textContent = "-";
    }
}

const desc = null;
const reply = null;
const ChatHistory = null;
const current_knowledge = null;
let if_r1 = true; // true:deepseek R1 模型  false:chatgtp 4o
// 获取工单详情，工单问题描述，工单问题回答，AI评价
function getOrderDetail() {
    axios.get(`${BASE_URL}/lg/caseinfo?creatby=${this.selectedId}&createtime_start=${this.selectedDate}&createtime_end=${this.selectDateStop}&caseid=${this.selectedOrderTitle}`)
        .then(function (response) {
            document.getElementById('AI_desc').classList.remove('active-green');
            document.getElementById('AI_kf_reply').classList.remove('AI-active-green');
            // console.log(response.data);
            document.getElementById('response1').style.display = "none"
            document.getElementById('problemdescription1').style.display = "none";
            document.getElementById('problemreply1').style.display = "none";
            // document.getElementById('chatRecord').style.display = "none";
            const charRecord = document.getElementById('chatRecord');
            if (charRecord) {
                charRecord.style.display = "none";
            }
            document.getElementById('response').style.display = "block"
            document.getElementById('problemdescription').style.display = "block";
            document.getElementById('problemreply').style.display = "block";

            document.getElementById('response').innerHTML = ""
            document.getElementById('problemdescription').innerHTML = response.data.problemdescription;
            this.desc = response.data.problemdescription;
            document.getElementById('pro_desc').classList.add('active-green');
            document.getElementById('problemreply').innerHTML = response.data.problemreply;
            this.reply = response.data.problemreply;
            document.getElementById('kf_reply').classList.add('AI-active-green');

            document.getElementById('call').innerHTML = response.data.caller;
            document.getElementById('calltime').innerHTML = response.data.calltime;
            document.getElementById('called').innerHTML = response.data.callee;

            document.getElementById('response').innerHTML = response.data.think;
            this.think = response.data.think;
            this.ai_comment = response.data.ai_comment;
            this.kf_reply = response.data.score;
            this.summer_reply = response.data.fit;

            // 获取当前工单的知识点
            this.current_knowledge = response.data.kb_content;

            // 转换聊天记录为string,赋值给续写按钮
            const array = response.data.transcription; // 假设这是你的数组
            this.ChatHistory = response.data.transcription
            let kbModal = [];

            // 获取容器
            const container = document.querySelector(".workInformation");
            // 清空旧的聊天内容
            container.innerHTML = '';
            // 确保 transcription 是数组
            if (Array.isArray(response.data.transcription)) {
                // 遍历消息数组，动态生成聊天内容
                response.data.transcription.forEach((item, index) => {
                    const talk = item.talk; // 获取 talk 属性
                    const text = item.text; // 获取 text 属性

                    // 如果消息为空，则跳过
                    if (text.trim() === "") return;

                    // 创建消息容器
                    const messageDiv = document.createElement("div");
                    messageDiv.classList.add("order_message");

                    // 判断消息方向（左右）
                    if (talk === "master") {
                        messageDiv.classList.add("right"); // 客服消息靠右
                    } else if (talk === "slave") {
                        messageDiv.classList.add("left"); // 用户消息靠左
                    } else {
                        console.warn("Unknown talk type:", talk);
                        return; // 如果 talk 类型未知，则跳过
                    }

                    // 创建头像
                    const avatar = document.createElement("div");
                    avatar.classList.add("avatar");
                    avatar.classList.add(talk === "master" ? "left" : "right");
                    avatar.textContent = talk === "master" ? "客" : "用"; // 客服显示“客”，用户显示“用”

                    // 创建消息文本
                    const textElement = document.createElement("div");
                    textElement.classList.add("text");
                    textElement.classList.add(talk === "master" ? "left" : "right");
                    textElement.textContent = text;

                    // 将头像和消息文本添加到消息容器
                    messageDiv.appendChild(avatar);
                    messageDiv.appendChild(textElement);

                    // 将消息容器添加到容器中
                    container.appendChild(messageDiv);
                    // 如果消息为 slave，则在消息容器之外添加两个按钮
                    if (talk === "slave") {
                        const btnContainer = document.createElement("div");
                        btnContainer.classList.add("slave-btn-container");

                        // 点击查询知识库
                        const btn1 = document.createElement("button");
                        btn1.textContent = "知识";
                        btn1.classList.add("slave-btn");
                        btn1.addEventListener("click", () => {
                            console.log("消息内容:", text);
                            axios.get(`${BASE_URL}/lg/search_kb?text=${text}`).then(function (response) {
                                console.log("KB内容:", response.data);
                                kbModal = response.data;
                                showModal(response.data);
                            });
                        });

                        // 点击进行AI客服续写
                        const btn2 = document.createElement("button");
                        btn2.textContent = "草拟";
                        btn2.classList.add("slave-btn");
                        btn2.addEventListener("click", async () => {
                            console.log("续写按钮点击，消息内容:", text);
                            // 删除当前消息（messageDiv）之后的所有兄弟节点
                            let nextSibling = messageDiv.nextElementSibling;
                            while (nextSibling) {
                                const temp = nextSibling.nextElementSibling;
                                nextSibling.remove();
                                nextSibling = temp;
                            }

                            // 生成续写内容
                            const newMessageDiv = document.createElement("div");
                            newMessageDiv.classList.add("order_message", "right"); // 与 mastermaster 消息一致
                            // 创建头像
                            const newAvatar = document.createElement("div");
                            newAvatar.classList.add("avatar", "left"); // 用户消息头像一般为右侧或根据实际情况调整
                            newAvatar.textContent = "客";
                            newMessageDiv.appendChild(newAvatar);
                            // 创建文本区域，初始为空，等待 SSE 数据填充
                            const newTextElement = document.createElement("div");
                            newTextElement.classList.add("text", "left");
                            newTextElement.textContent = "思考中...";
                            newMessageDiv.appendChild(newTextElement);
                            // 将新生成的消息插入到容器中，紧随原来的 messageDiv 之后
                            container.insertBefore(newMessageDiv, messageDiv.nextElementSibling);
                            const response = await axios.get(`${BASE_URL}/lg/search_kb?text=${text}`);
                            kbModal = response.data;

                            try {
                                console.log("续写按钮点击，消息内容:", this.if_r1);
                                // 发送POST请求
                                const response = await fetch(`${BASE_URL}/lg/generate_current_reply`, {
                                    method: 'POST',
                                    headers: {
                                        'Content-Type': 'application/json'
                                    },
                                    body: JSON.stringify({ user_input: text, chat_history: array, kb_content: kbModal, if_r1: this.if_r1 })
                                });
                                if (!response.ok) {
                                    throw new Error('Network response was not ok');
                                }
                                const reader = response.body.getReader();
                                const decoder = new TextDecoder();
                                let accumulatedMessage = "";
                                async function read() {
                                    const { done, value } = await reader.read();
                                    if (done) {
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
                                                    // console.log('data:', data);
                                                    accumulatedMessage += data;
                                                    if (accumulatedMessage.startsWith('<think>')) {
                                                        // 如果内容以 <think> 开头，则按原逻辑处理
                                                        // accumulatedMessage += data;

                                                        // 检测 </think> 标签，如果存在，在其后添加换行符
                                                        if (accumulatedMessage.includes('</think>')) {
                                                            accumulatedMessage = accumulatedMessage.replace('</think>', '</think>\n');
                                                        }

                                                        // 提取 </think> 之后的内容
                                                        const thinkEnd = accumulatedMessage.indexOf('</think>');
                                                        if (thinkEnd !== -1) {
                                                            const afterThinkContent = accumulatedMessage.substring(thinkEnd + 7).trim();
                                                            newTextElement.innerHTML = this.md.render(afterThinkContent);
                                                        }
                                                    } else {
                                                        // 如果不以 <think> 开头，则直接渲染数据
                                                        newTextElement.innerHTML = this.md.render(accumulatedMessage);
                                                    }
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
                        });

                        btnContainer.appendChild(btn1);
                        btnContainer.appendChild(btn2);
                        // 按钮放在消息容器之后（外部）
                        messageDiv.appendChild(btnContainer);
                    }
                });
            } else {
                console.error("score is not an array:", response.data.score);
            }
            fetchKnowledge()
            fetchsummery()
            // 自动触发“思维链”按钮的点击
            const thinkButton = document.getElementById('show-think');
            if (thinkButton) {
                thinkButton.click();
            }
        })
}

// 知识库 弹框生成函数，支持显示多个结果
function showModal(dataArray) {
    console.log('showModal called with data:', dataArray);
    // 若已有弹框，则先移除
    const existingModal = document.getElementById('kb-modal');
    if (existingModal) {
        existingModal.remove();
    }

    // 创建弹框容器
    const modal = document.createElement('div');
    modal.id = 'kb-modal';
    modal.style.position = 'fixed';
    modal.style.top = '50%';
    modal.style.left = '50%';
    modal.style.height = '60%';
    modal.style.transform = 'translate(-50%, -50%)';
    modal.style.backgroundColor = '#fff';
    modal.style.padding = '20px';
    modal.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
    modal.style.zIndex = '10000';
    modal.style.width = '400px';
    modal.style.borderRadius = '8px';
    modal.style.fontFamily = 'Arial, sans-serif';
    modal.style.textAlign = 'left'; // 默认左对齐，标题可以居中
    modal.style.maxHeight = '80vh';
    modal.style.overflowY = 'auto';

    // 创建右上角关闭按钮
    const closeButton = document.createElement('button');
    closeButton.textContent = '×';
    closeButton.style.position = 'absolute';
    closeButton.style.top = '10px';
    closeButton.style.right = '10px';
    closeButton.style.border = 'none';
    closeButton.style.background = 'transparent';
    closeButton.style.fontSize = '20px';
    closeButton.style.cursor = 'pointer';
    closeButton.style.color = 'black';
    closeButton.addEventListener('click', () => {
        modal.remove();
    });
    modal.appendChild(closeButton);

    // 如果 dataArray 为数组，则遍历每条结果显示
    if (Array.isArray(dataArray)) {
        dataArray.forEach(item => {
            // 每条结果的容器，可设置下边框作区分
            const itemContainer = document.createElement('div');
            itemContainer.style.borderBottom = '1px solid #eee';
            itemContainer.style.padding = '10px 0';
            // 标题（显示在最上方，居中显示）
            const titleEl = document.createElement('h2');
            titleEl.textContent = item.title || '无标题';
            titleEl.style.fontSize = '18px';
            titleEl.style.margin = '10px 0';
            itemContainer.appendChild(titleEl);

            // 内容（中间部分）
            const contentEl = document.createElement('p');
            contentEl.textContent = item.content || '无内容';
            contentEl.style.margin = '10px 0';
            itemContainer.appendChild(contentEl);

            // 相似度显示（内容下面）
            const similarityEl = document.createElement('div');
            similarityEl.textContent = `相似度: ${item.similarity !== undefined ? item.similarity : '未知'}`;
            similarityEl.style.fontWeight = 'bold';
            similarityEl.style.textAlign = 'right';
            itemContainer.appendChild(similarityEl);

            modal.appendChild(itemContainer);
        });
    } else {
        // 如果返回的不是数组，则按单条结果显示
        const titleEl = document.createElement('h2');
        titleEl.textContent = dataArray.title || '无标题';
        titleEl.style.fontSize = '18px';
        titleEl.style.margin = '10px 0';
        modal.appendChild(titleEl);

        const contentEl = document.createElement('p');
        contentEl.textContent = dataArray.content || '无内容';
        contentEl.style.margin = '10px 0';
        modal.appendChild(contentEl);

        const similarityEl = document.createElement('div');
        similarityEl.textContent = `相似度: ${dataArray.similarity || '未知'}`;
        similarityEl.style.fontWeight = 'bold';
        similarityEl.style.textAlign = 'right';
        modal.appendChild(similarityEl);
    }

    // 将弹框添加到页面中
    document.body.appendChild(modal);
}

let if_kb_QA = false;
// 是否开启知识库
function toggleKnowledge(checkbox_ai) {
    if (checkbox_ai.checked) {
        this.if_kb_QA = true;
        console.log('开启知识库', this.if_kb_QA)
    } else {
        this.if_kb_QA = false;
        console.log('关闭知识库', this.if_kb_QA)
    }
}

// 是否开R1
function toggleKnowledgeR1(checkbox_r1) {
    if (checkbox_r1.checked) {
        this.if_r1 = true;
        console.log('开启知识库', this.if_r1)
    } else {
        this.if_r1 = false;
        console.log('关闭知识库', this.if_r1)

    }
}

// 个案问答 --- chat
async function QAsendMessage() {
    const input = document.getElementById('chat-input');
    const messageText = input.innerHTML;
    // const rendermessage = this.md.render(messageText);
    // console.log(messageText)
    localStorage.setItem('hasSentMessage', 'true');
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
        // console.log('发送成功', this.chat_id)
        try {
            // 发送POST请求
            const response = await fetch(`${BASE_URL}/lg/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ user_input: messageText, chat_type: '0', if_kb: this.if_kb_QA, case_id: this.selectedOrderTitle, case_date_begin: this.selectedDate, case_date_end: this.selectDateStop, case_create_by: this.selectedId, case_problem_description: 'string', chat_id: 'f47e1111-1111-1111-1111-111111111111' })
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
                <div class="message-content">
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

                                // 检测 </think> 标签，如果存在，在其后添加换行符
                                if (accumulatedMessage.includes('</think>')) {
                                    accumulatedMessage = accumulatedMessage.replace('</think>', '</think>\n');
                                }

                                // 使用 marked.js 将 Markdown 转换为 HTML
                                // 但保留 <think> 和 </think> 标签
                                const htmlContent = this.md.render(accumulatedMessage.replace(/</g, '&lt;').replace(/>/g, '&gt;'));

                                // 更新机器人消息内容
                                messageTextContainer.innerHTML = htmlContent;

                                // 设置播放按钮的点击事件
                                playButton.setAttribute('onclick', `bf_vedio('${uniqueId}', '${accumulatedMessage}')`);

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

// </think>之后的输出内容
let afterThinkContent = null;
// 问题提取 --- chat
async function sendMessagequestion() {
    const input = document.getElementById('chat-input');
    const messageText = input.innerHTML;
    if (messageText && this.ChatHistory) {
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
        // console.log('发送成功', this.chat_id)
        try {
            // 发送POST请求
            const response = await fetch(`${BASE_URL}/lg/extract_issues`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ user_input: "string", chat_history: this.ChatHistory, if_r1: this.if_r1 })
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
                <div class="message-content">
                    <div class="message-text">${accumulatedMessage}</div>
                    <i class="fa-regular fa-circle-play" id="play_${uniqueId}" style="display:none;" onclick="bf_vedio('${uniqueId}', '${accumulatedMessage}')"></i>
                    <i class="fa-regular fa-circle-pause" style="display:none" id="pause_${uniqueId}" onclick="zt_vedio('${uniqueId}')"></i>
                    <audio id="${uniqueId}" style="display:none"></audio>
                </div>
            `;
            document.getElementById('chat-messages').appendChild(botMessage);
            // 获取消息文本容器
            const messageTextContainer = botMessage.querySelector('.message-text');
            async function read() {
                const { done, value } = await reader.read();
                if (done) {
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
                                // 累积AI消息数据
                                accumulatedMessage += data;

                                // 如果以 <think> 开头，则检测是否存在 </think> 标签
                                if (accumulatedMessage.startsWith('<think>')) {
                                    if (accumulatedMessage.includes('</think>')) {
                                        accumulatedMessage = accumulatedMessage.replace('</think>', '</think>\n');
                                    }
                                }
                                // 使用 marked.js 将 Markdown 转换为 HTML，
                                // 同时将 < 和 > 转义为实体字符
                                const htmlContent = this.md.render(accumulatedMessage.replace(/</g, '&lt;').replace(/>/g, '&gt;'));

                                // 更新机器人消息内容
                                messageTextContainer.innerHTML = this.md.render(htmlContent);

                                // 提取 </think> 之后的内容
                                const thinkEnd = accumulatedMessage.indexOf('</think>');
                                if (thinkEnd !== -1) {
                                    this.afterThinkContent = accumulatedMessage.substring(thinkEnd + 7).trim();
                                } else {
                                    this.afterThinkContent = accumulatedMessage;
                                }
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
    } else {
        showMessage('请输入问题或选中工单');
    }
}

// 知识整理 --- chat
async function sendMessagedemoknowledge() {
    const input = document.getElementById('chat-input');
    const messageText = input.innerHTML;

    if (messageText && this.afterThinkContent) {
        // 将 afterThinkContent 拆分为数组
        const contentArray = this.afterThinkContent
            .split('\n')                           // 按换行符拆分
            .map(item => item.trim())              // 去掉两边空白
            .filter(item => item.length > 0);
        const filteredArr = contentArray.filter(item => item.trim() !== '>');

        // 取第一个非">"的字符串
        const content = filteredArr[0];

        // 以数字加点作为分隔符进行拆分，并过滤掉首尾空字符串
        const questions = content
            .split(/\d\./)
            .map(item => item.trim())
            .filter(item => item.length > 0);

        console.log("contentArray:", questions);

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
        // console.log('发送成功', this.chat_id)
        try {
            // 发送POST请求
            const response = await fetch(`${BASE_URL}/lg/generate_extract_issues_reply_by_kb`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ chat_history: this.ChatHistory, issues: questions, if_r1: this.if_r1, kb_content: this.current_knowledge })
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
                <div class="message-content">
                    <div class="message-text">${accumulatedMessage}</div>
                    <i class="fa-regular fa-circle-play" id="play_${uniqueId}" style="display:none;" onclick="bf_vedio('${uniqueId}', '${accumulatedMessage}')"></i>
                    <i class="fa-regular fa-circle-pause" style="display:none" id="pause_${uniqueId}" onclick="zt_vedio('${uniqueId}')"></i>
                    <audio id="${uniqueId}" style="display:none"></audio>
                </div>
            `;
            document.getElementById('chat-messages').appendChild(botMessage);
            // 获取消息文本容器
            const messageTextContainer = botMessage.querySelector('.message-text');
            async function read() {
                const { done, value } = await reader.read();
                if (done) {
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
                            if (data !== undefined) {
                                // 累积AI消息
                                accumulatedMessage += data;

                                // // 如果内容以 <think> 开头，则检测是否包含 </think> 标签，并在其后添加换行符
                                // if (accumulatedMessage.startsWith('<think>')) {
                                //     if (accumulatedMessage.includes('</think>')) {
                                //         accumulatedMessage = accumulatedMessage.replace(/<\/think>(?!\n)/g, '</think>\n');
                                //     }
                                // }

                                // 使用 marked.js 将 Markdown 转换为 HTML，并将 < 和 > 转义为实体字符
                                const htmlContent = this.md.render(accumulatedMessage.replace(/</g, '&lt;').replace(/>/g, '&gt;'));

                                // 更新机器人消息内容
                                messageTextContainer.innerHTML = this.md.render(htmlContent);

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
    } else {
        showMessage('请输入问题或已获取到问题提取结果');
    }
}

const AI_problem_desc = null;
// 问题描述
document.getElementById('pro_desc').addEventListener('click', (event) => {
    console.log('点击了问题描述', this.desc);
    // 因为箭头函数无法绑定自己的this,所以用使用 event.currentTarget 替代 this
    event.currentTarget.classList.add('active-green');
    // 移除另一个元素的绿色样式
    document.getElementById('AI_desc').classList.remove('active-green');

    const problemdescription = document.getElementById('problemdescription');
    problemdescription.style.display = 'block';
    problemdescription.innerHTML = this.desc || "暂无内容";
    document.getElementById('problemdescription1').style.display = 'none';
    document.getElementById('AI_problemdescription').style.display = 'none';
});

// AI问题描述
async function AI_QAsendMessage() {
    const input = document.getElementById('chat-input');
    const messageText = input.innerHTML;
    localStorage.setItem('hasSentMessage', 'true');
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
        console.log('发送成功', this.chat_id)
        try {
            // 发送POST请求
            const response = await fetch(`${BASE_URL}/lg/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ user_input: messageText, chat_type: '0', if_kb: this.if_kb_QA, case_id: this.selectedOrderTitle, case_date_begin: this.selectedDate, case_date_end: this.selectDateStop, case_create_by: this.selectedId, case_problem_description: 'string', chat_id: 'f47e1111-1111-1111-1111-111111111111' })
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
                <div class="message-content">
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

                                // 检测 </think> 标签，如果存在，在其后添加换行符
                                if (accumulatedMessage.includes('</think>')) {
                                    accumulatedMessage = accumulatedMessage.replace('</think>', '</think>\n');
                                }

                                // 使用 marked.js 将 Markdown 转换为 HTML
                                // 但保留 <think> 和 </think> 标签
                                const htmlContent = this.md.render(accumulatedMessage.replace(/</g, '&lt;').replace(/>/g, '&gt;'));

                                // 检测 </think> 标签，提取其后的内容
                                const thinkEnd = accumulatedMessage.indexOf('</think>');
                                if (thinkEnd !== -1) {
                                    // 提取 </think> 之后的内容
                                    const afterThinkContent = accumulatedMessage.substring(thinkEnd + 7).trim();

                                    // 更新 AI_problemdescription 标签的内容
                                    const problemdescription = document.getElementById('AI_problemdescription');
                                    if (problemdescription) {
                                        problemdescription.style.display = 'block';
                                        document.getElementById('problemdescription').style.display = 'none';
                                        document.getElementById('problemdescription1').style.display = 'none';
                                        problemdescription.textContent = afterThinkContent;
                                        this.AI_problem_desc = afterThinkContent.trim();
                                        console.log('AI_problem_desc', this.AI_problem_desc)
                                    }
                                }

                                // 更新机器人消息内容
                                messageTextContainer.innerHTML = htmlContent;

                                // 设置播放按钮的点击事件
                                playButton.setAttribute('onclick', `bf_vedio('${uniqueId}', '${accumulatedMessage}')`);

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

// ai问题描述
document.getElementById('AI_desc').addEventListener('click', (event) => {
    // 为当前元素添加绿色样式
    // 因为箭头函数无法绑定自己的this,所以用使用 event.currentTarget 替代 this
    event.currentTarget.classList.add('active-green');
    // 移除另一个元素的绿色样式
    document.getElementById('pro_desc').classList.remove('active-green');

    console.log('点击了AI问题描述', this.AI_problem_desc);
    if (this.AI_problem_desc) {
        const problemdescription = document.getElementById('AI_problemdescription');
        problemdescription.style.display = 'block';
        problemdescription.innerHTML = this.md.render(this.AI_problem_desc);
        document.getElementById('problemdescription').style.display = 'none';
        document.getElementById('problemdescription1').style.display = 'none';
    } else {
        switchPanel('qa', false);
        document.getElementById('send-button_QA').style.display = 'block';
        document.getElementById('send-button').style.display = 'none';
        document.getElementById('qa_messages').style.display = 'block';

        document.getElementById('data_messages').style.display = 'none';
        document.getElementById('qa-button').style.display = 'block';
        document.getElementById('data-button').style.display = 'none';

        document.getElementById('knowledge_data_messages').style.display = 'none';
        document.getElementById('Q-data-button').style.display = 'none';
        document.getElementById('send-button-knowledge').style.display = 'none';
        const recordButton = document.getElementById('record_button');
        recordButton.style.backgroundColor = '#1FDE82';
        document.getElementById('chat-input').innerHTML = '请根据聊天记录生成简单的问题描述';
        AI_QAsendMessage();
    }
});

// 客服回复
document.getElementById('kf_reply').addEventListener('click', (event) => {
    console.log('点击了客服回复', this.reply);
    // 因为箭头函数无法绑定自己的this,所以用使用 event.currentTarget 替代 this
    event.currentTarget.classList.add('AI-active-green');
    // 移除另一个元素的绿色样式
    document.getElementById('AI_kf_reply').classList.remove('AI-active-green');
    const kfreply = document.getElementById('problemreply');
    kfreply.style.display = 'block';
    kfreply.innerHTML = this.reply || "暂无内容";
    document.getElementById('problemreply1').style.display = 'none';
    document.getElementById('AI_problemreply').style.display = 'none';
});

const AI_kf_Reply = null;
// AI客服回复
async function AI_QAsendMessage_reply() {
    const input = document.getElementById('chat-input');
    const messageText = input.innerHTML;
    localStorage.setItem('hasSentMessage', 'true');
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
        console.log('发送成功', this.chat_id)
        try {
            // 发送POST请求
            const response = await fetch(`${BASE_URL}/lg/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ user_input: messageText, chat_type: '0', if_kb: this.if_kb_QA, case_id: this.selectedOrderTitle, case_date_begin: this.selectedDate, case_date_end: this.selectDateStop, case_create_by: this.selectedId, case_problem_description: 'string', chat_id: 'f47e1111-1111-1111-1111-111111111111' })
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
                <div class="message-content">
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
                // console.log(lines)
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

                                // 检测 </think> 标签，如果存在，在其后添加换行符
                                if (accumulatedMessage.includes('</think>')) {
                                    accumulatedMessage = accumulatedMessage.replace('</think>', '</think>\n');
                                }

                                // 使用 marked.js 将 Markdown 转换为 HTML
                                // 但保留 <think> 和 </think> 标签
                                const htmlContent = this.md.render(accumulatedMessage.replace(/</g, '&lt;').replace(/>/g, '&gt;'));

                                // 检测 </think> 标签，提取其后的内容
                                const thinkEnd = accumulatedMessage.indexOf('</think>');
                                if (thinkEnd !== -1) {
                                    // 提取 </think> 之后的内容
                                    const afterThinkContent = accumulatedMessage.substring(thinkEnd + 7).trim();

                                    // 更新 AI_problemdescription 标签的内容
                                    const KF_Reply_content = document.getElementById('AI_problemreply');
                                    if (KF_Reply_content) {
                                        KF_Reply_content.style.display = 'block';
                                        document.getElementById('problemreply').style.display = 'none';
                                        document.getElementById('problemreply1').style.display = 'none';
                                        KF_Reply_content.textContent = afterThinkContent;
                                        this.AI_kf_Reply = afterThinkContent.trim();
                                    }
                                }

                                // 更新机器人消息内容
                                messageTextContainer.innerHTML = htmlContent;

                                // 设置播放按钮的点击事件
                                playButton.setAttribute('onclick', `bf_vedio('${uniqueId}', '${accumulatedMessage}')`);

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
// ai客服回复
document.getElementById('AI_kf_reply').addEventListener('click', (event) => {
    console.log('点击了AI客服回复', this.AI_kf_Reply);
    // 因为箭头函数无法绑定自己的this,所以用使用 event.currentTarget 替代 this
    event.currentTarget.classList.add('AI-active-green');
    // 移除另一个元素的绿色样式
    document.getElementById('kf_reply').classList.remove('AI-active-green');
    if (this.AI_kf_Reply) {
        const kfreply = document.getElementById('AI_problemreply');
        kfreply.style.display = 'block';
        kfreply.innerHTML = this.md.render(this.AI_kf_Reply);
        document.getElementById('problemreply1').style.display = 'none';
        document.getElementById('problemreply').style.display = 'none';
    } else {
        // 请根据聊天记录生成简单的客服回复
        // 默认选中 QA 问答区域
        switchPanel('qa', false);
        document.getElementById('send-button_QA').style.display = 'block';
        document.getElementById('send-button').style.display = 'none';
        document.getElementById('qa_messages').style.display = 'block';

        document.getElementById('data_messages').style.display = 'none';
        document.getElementById('qa-button').style.display = 'block';
        document.getElementById('data-button').style.display = 'none';

        document.getElementById('knowledge_data_messages').style.display = 'none';
        document.getElementById('Q-data-button').style.display = 'none';
        document.getElementById('send-button-knowledge').style.display = 'none';
        const recordButton = document.getElementById('record_button');
        recordButton.style.backgroundColor = '#1FDE82';
        document.getElementById('chat-input').innerHTML = '请根据聊天记录生成简单的客服回复';
        AI_QAsendMessage_reply();
    }
});

// 防抖处理函数
function debounce(func, delay) {
    let timeout;
    return function (...args) {
        const context = this;
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            func.apply(context, args);
        }, delay);
    }
}

window.onload = function () {
    // 创建 markdown-it 实例并注册 task-lists 插件
    this.md = window
        .markdownit({
            html: true,
            linkify: true,
            typographer: true,
            breaks: true
        })
        .use(window.markdownitTaskLists, {
            enabled: true,
            label: true,
            labelAfter: true,
        });
}