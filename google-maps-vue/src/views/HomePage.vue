<!-- src/views/HomePage.vue -->
<template>
    <transition name="fade" appear>
        <GoogleMap class="map animated fadeIn" @borrowLocationUpdated="updateBorrowLocation"
            @returnLocationUpdated="updateReturnLocation" :borrowLocation="borrowLocation"
            :returnLocation="returnLocation" :borrowRecommendedLocation="borrowRecommendedLocation" :returnRecommendedLocation="returnRecommendedLocation" :formData="formData" />
    </transition>
    <transition name="fade" appear>
        <form @submit.prevent="handleSubmit" class="form-container">
            <div v-if="formData.search_type === '1' || formData.search_type === '2'" class="form-group mb-3">
                <label for="borrow_date" class="form-label">預定借車日期:</label>
                <input type="date" id="borrow_date" class="form-control" v-model="formData.borrow_date"
                    :min="borrow_minDate" :max="borrow_maxDate" required @change="handleBorrowDateChange" />
            </div>
            <div v-if="formData.search_type === '1' || formData.search_type === '2'" class="form-group mb-3">
                <label for="borrow_time" class="form-label">預定借車時間:</label>
                <input type="time" id="borrow_time" class="form-control" v-model="formData.borrow_time"
                    :min="borrow_minTime" :max="borrow_maxTime" required @change="handleBorrowDateChange" />
            </div>
            <div v-if="formData.search_type === '1' || formData.search_type === '3'" class="form-group mb-3">
                <label for="return_date" class="form-label">預定還車日期:</label>
                <input type="date" id="return_date" class="form-control" v-model="formData.return_date"
                    :min="return_minDate" required @change="handleReturnDateChange" />
            </div>
            <div v-if="formData.search_type === '1' || formData.search_type === '3'" class="form-group mb-3">
                <label for="return_time" class="form-label">預定還車時間:</label>
                <input type="time" id="return_time" class="form-control" v-model="formData.return_time"
                    :min="return_minTime" required @change="handleReturnDateChange" />
            </div>
            <div class="form-group mb-3">
                <label for="search_type" class="form-label">查詢方式:</label>
                <select id="search_type" class="form-select" v-model="formData.search_type" @change="handleTypeChange">
                    <option selected value="1">借還站查詢</option>
                    <option value="2">借站查詢</option>
                    <option value="3">還站查詢</option>
                </select>
            </div>
            <button type="submit" class="btn btn-primary">送出</button>
        </form>
    </transition>
    <transition name="fade" appear>
        <div class="query-history container mt-4 p-4">
            <h3 class="mb-3 text-center text-white">查詢紀錄</h3>
            <div v-if="queryHistory.length === 0" class="text-center">
                <p class="text-white">目前沒有查詢紀錄</p>
            </div>
            <div v-else class="row">
                <div v-for="(query, index) in paginatedHistory" :key="index" class="col-md-6 mb-3">
                    <div class="card animate__animated animate__fadeInUp" :class="'color-' + (index % 5)">
                        <div class="card-header text-white">
                            <strong>查詢時間: {{ query.date }} {{ query.time }} </strong>
                        </div>
                        <div class="card-body">
                            <p class="card-text"><strong>借車時間：</strong>{{ query.borrow_date }} {{ query.borrow_time }}</p>
                            <p class="card-text"><strong>推薦借車地點一：</strong>{{ query.recommendedLocation[0].station[0] }}</p>
                            <p class="card-text"><strong>車站距離：</strong>{{ Math.round(query.recommendedLocation[0].distance[0]*1000) / 1000 }} 公里(km)</p>
                            <p class="card-text"><strong>推薦借車地點二：</strong>{{ query.recommendedLocation[0].station[1] }}</p>
                            <p class="card-text"><strong>車站距離：</strong>{{ Math.round(query.recommendedLocation[0].distance[1]*1000) / 1000 }} 公里(km)</p>
                            <p class="card-text"><strong>推薦借車地點三：</strong>{{ query.recommendedLocation[0].station[2] }}</p>
                            <p class="card-text"><strong>車站距離：</strong>{{ Math.round(query.recommendedLocation[0].distance[2]*1000) / 1000 }} 公里(km)</p>
                            <p class="card-text"><strong>還車時間：</strong>{{ query.return_date }} {{ query.return_time }}</p>
                            <p class="card-text"><strong>推薦還車地點一：</strong>{{ query.recommendedLocation[1].station[0] }}</p>
                            <p class="card-text"><strong>車站座標：</strong>{{ Math.round(query.recommendedLocation[1].distance[0]*1000) / 1000 }} 公里(km)</p>
                            <p class="card-text"><strong>推薦還車地點二：</strong>{{ query.recommendedLocation[1].station[1] }}</p>
                            <p class="card-text"><strong>車站座標：</strong>{{ Math.round(query.recommendedLocation[1].distance[1]*1000) / 1000 }} 公里(km)</p>
                            <p class="card-text"><strong>推薦還車地點三：</strong>{{ query.recommendedLocation[1].station[2] }}</p>
                            <p class="card-text"><strong>車站座標：</strong>{{ Math.round(query.recommendedLocation[1].distance[2]*1000) / 1000 }} 公里(km)</p>
                        </div>
                    </div>
                </div>
            </div>
            <div v-if="totalPages > 1" class="pagination-container mt-4">
                <ul class="pagination justify-content-center">
                    <li :class="['page-item', { disabled: currentPage === 1 }]">
                        <a class="page-link" href="#" @click.prevent="prevPage">上一頁</a>
                    </li>
                    <li v-for="page in totalPages" :key="page" :class="['page-item', { active: page === currentPage }]">
                        <a class="page-link" href="#" @click.prevent="goToPage(page)">{{ page }}</a>
                    </li>
                    <li :class="['page-item', { disabled: currentPage === totalPages }]">
                        <a class="page-link" href="#" @click.prevent="nextPage">下一頁</a>
                    </li>
                </ul>
            </div>
        </div>
    </transition>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import GoogleMap from '../components/GoogleMap.vue';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'animate.css/animate.min.css';

export default {
    name: 'App',
    components: {
        GoogleMap,
    },
    setup() {
        const formData = ref({ borrow_date: '', borrow_time: '', return_date: '', return_time: '', search_type: '1' });
        const borrowLocation = ref(null);
        const returnLocation = ref(null);
        const borrowRecommendedLocation = ref(null);
        const returnRecommendedLocation = ref(null);
        const borrow_minDate = ref(new Date().toISOString().split('T')[0]);
        const borrow_minTime = ref(new Date().toLocaleTimeString('it-IT').slice(0, 5));
        const return_minDate = ref(new Date().toISOString().split('T')[0]);
        const return_minTime = ref(new Date().toLocaleTimeString('it-IT').slice(0, 5));
        const borrow_maxDate = ref(return_minDate.value);
        const borrow_maxTime = ref(return_minTime.value);
        const queryHistory = ref([]); // 用於存儲查詢紀錄

        // 分頁設置
        const itemsPerPage = 2;
        const currentPage = ref(1);

        const totalPages = computed(() => Math.ceil(queryHistory.value.length / itemsPerPage));

        const paginatedHistory = computed(() => {
            const start = (currentPage.value - 1) * itemsPerPage;
            const end = start + itemsPerPage;
            return queryHistory.value.slice(start, end);
        });

        const nextPage = () => {
            if (currentPage.value < totalPages.value) {
                currentPage.value++;
            }
        };

        const prevPage = () => {
            if (currentPage.value > 1) {
                currentPage.value--;
            }
        };

        const goToPage = (page) => {
            currentPage.value = page;
        };

        onMounted(() => {

            const now = new Date();
            formData.value.borrow_date = now.toISOString().split('T')[0];
            formData.value.borrow_time = now.toLocaleTimeString('it-IT').slice(0, 5);
            formData.value.return_date = now.toISOString().split('T')[0];
            formData.value.return_time = now.toLocaleTimeString('it-IT').slice(0, 5);
            formData.value.search_type = "1";

            returnLocation.value = {
                lat: 25.0332,
                lng: 121.5743
            };
            borrowLocation.value = {
                lat: 25.042,
                lng: 121.5433
            };

            // 從本地存儲中讀取查詢紀錄
            loadQueryHistory();
            // 移除過時的紀錄
            removeExpiredQueries();
        });

        const handleSubmit = async () => {
            if (!borrowLocation.value) {
                alert('無法獲取使用者位置');
                return;
            }

            const data = {
                borrow_date: formData.value.borrow_date,
                borrow_time: formData.value.borrow_time,
                return_date: formData.value.return_date,
                return_time: formData.value.return_time,
                search_type: formData.value.search_type,
                returnLocation: returnLocation.value,
                borrowLocation: borrowLocation.value
            };

            try {
                const response = await fetch('http://127.0.0.1/api/recommend', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });

                if (!response.ok) {
                    alert('查詢失敗，請稍後再試。');
                    throw new Error('Network response was not ok');
                }

                const result = await response.json();

                // 確保經緯度值是有效的數字
                if (formData.value.search_type == "1" && 
                    result[0].location.lat && result[0].location.lng && !isNaN(result[0].location.lat[0]) && !isNaN(result[0].location.lng[0]) && !isNaN(result[0].location.lat[1]) && !isNaN(result[0].location.lng[1]) && !isNaN(result[0].location.lat[2]) && !isNaN(result[0].location.lng[2]) &&
                    result[1].location.lat && result[1].location.lng && !isNaN(result[1].location.lat[0]) && !isNaN(result[1].location.lng[0]) && !isNaN(result[1].location.lat[1]) && !isNaN(result[1].location.lng[1]) && !isNaN(result[1].location.lat[2]) && !isNaN(result[1].location.lng[2])) {
                    borrowRecommendedLocation.value = {
                        lat: result[0].location.lat,
                        lng: result[0].location.lng,
                        station: result[0].station,
                        distance: result[0].distance,
                        predicted_available_bikes: result[0].predicted_available_bikes
                    };

                    returnRecommendedLocation.value = {
                        lat: result[1].location.lat,
                        lng: result[1].location.lng,
                        station: result[1].station,
                        distance: result[1].distance,
                        predicted_available_bikes: result[1].predicted_available_return
                    };
                    // 保存查詢紀錄到本地存儲
                    saveQueryToHistory(data, [borrowRecommendedLocation.value,returnRecommendedLocation.value]);

                    // 滾動到地圖位置
                    scrollToMap();
                }else if (formData.value.search_type == "2" && result[0].location.lat && result[0].location.lng && !isNaN(result[0].location.lat) && !isNaN(result[0].location.lng)) {
                    borrowRecommendedLocation.value = {
                        lat: parseFloat(result[0].location.lat),
                        lng: parseFloat(result[0].location.lng),
                        station: result[0].station,
                        distance: result[0].distance,
                        predicted_available_bikes: result[0].predicted_available_bikes
                    };

                    returnRecommendedLocation.value = {
                        lat: "無",
                        lng: "無",
                        station: "無",
                        distance: "無",
                        predicted_available_bikes: "無"
                    };
                    // 保存查詢紀錄到本地存儲
                    saveQueryToHistory(data, [borrowRecommendedLocation.value,returnRecommendedLocation.value]);

                    // 滾動到地圖位置
                    scrollToMap();
                }else if (formData.value.search_type == "3" && result[0].location.lat && result[0].location.lng && !isNaN(result[0].location.lat) && !isNaN(result[0].location.lng)) {
                    returnRecommendedLocation.value = {
                        lat: parseFloat(result[0].location.lat),
                        lng: parseFloat(result[0].location.lng),
                        station: result[0].station,
                        distance: result[0].distance,
                        predicted_available_bikes: result[0].predicted_available_bikes
                    };

                    borrowRecommendedLocation.value = {
                        lat: "無",
                        lng: "無",
                        station: "無",
                        distance: "無",
                        predicted_available_bikes: "無"
                    };
                    // 保存查詢紀錄到本地存儲
                    saveQueryToHistory(data, [borrowRecommendedLocation.value,returnRecommendedLocation.value]);

                    // 滾動到地圖位置
                    scrollToMap();
                }
                else {
                    console.error('Invalid coordinates received from the API');
                }
            } catch (error) {
                console.error('Error submitting data:', error);
            }
        };

        const Compare_time = (time1, time2) => {

            let time1Parts = time1.split(":");
            let time2Parts = time2.split(":");

            if (time1Parts[0] > time2Parts[0]) {
                return 1
            } else if (time1Parts[0] < time2Parts[0]) {
                return 0
            } else {
                // Hours are equal, compare minutes
                if (time1Parts[1] > time2Parts[1]) {
                    return 1
                } else if (time1Parts[1] < time2Parts[1]) {
                    return -1
                }
            }
        }

        const updateBorrowLocation = (location) => {
            borrowLocation.value = location;
        };

        const updateReturnLocation = (location) => {
            returnLocation.value = location;
        };

        const handleBorrowDateChange = () => {
            const selectedBorrowDate = new Date(formData.value.borrow_date);
            const selectedReturnDate = new Date(formData.value.return_date);
            const today = new Date();
            return_minDate.value = formData.value.borrow_date
            // 處理時間是今天時間不能夠選擇過去的 小時:分鐘
            if (selectedBorrowDate.toDateString() === today.toDateString()) {
                borrow_minTime.value = today.toLocaleTimeString('it-IT', { hour12: false }).slice(0, 5);
                if (!Compare_time(formData.value.borrow_time, today.toLocaleTimeString('it-IT', { hour12: false }).slice(0, 5))) {
                    formData.value.borrow_time = today.toLocaleTimeString('it-IT', { hour12: false }).slice(0, 5)
                }
            } else {
                borrow_minTime.value = '00:00';
            }

            if (formData.value.search_type == "1" && selectedBorrowDate.toDateString() === selectedReturnDate.toDateString()) { // 同天
                return_minTime.value = borrow_minTime.value;
                if (Compare_time(formData.value.borrow_time, formData.value.return_time)) {
                    formData.value.borrow_time = formData.value.return_time
                }
                else {
                    borrow_maxTime.value = formData.value.return_time;
                }
            } else { // 不同天
                borrow_maxTime.value = "23:59";
                return_minTime.value = "00:00";
            }
        };

        const handleReturnDateChange = () => {
            const selectedBorrowDate = new Date(formData.value.borrow_date);
            const selectedReturnDate = new Date(formData.value.return_date);
            const today = new Date();
            borrow_maxDate.value = formData.value.return_date
            // 處理時間是今天時間不能夠選擇過去的 小時:分鐘
            if (selectedReturnDate.toDateString() === today.toDateString()) {
                return_minTime.value = today.toLocaleTimeString('it-IT', { hour12: false }).slice(0, 5);
                if (!Compare_time(formData.value.return_time, today.toLocaleTimeString('it-IT', { hour12: false }).slice(0, 5))) {
                    formData.value.return_time = today.toLocaleTimeString('it-IT', { hour12: false }).slice(0, 5)
                }
                if (formData.value.search_type == "1" && selectedBorrowDate.toDateString() === selectedReturnDate.toDateString()) { // 同天
                    if (Compare_time(formData.value.borrow_time, formData.value.return_time)) {
                        formData.value.return_time = formData.value.borrow_time
                    }
                    else {
                        borrow_maxTime.value = formData.value.return_time;
                    }
                }
                else // 不同天
                {
                    borrow_maxTime.value = "23:59";
                    return_minTime.value = '00:00';
                }
            } else if (formData.value.search_type == "1") { // 同天
                if (selectedBorrowDate.toDateString() === selectedReturnDate.toDateString()) {

                    if (Compare_time(formData.value.borrow_time, formData.value.return_time)) {
                        formData.value.return_time = formData.value.borrow_time
                    }
                    else {
                        borrow_maxTime.value = formData.value.return_time;
                    }
                }
                else // 不同天
                {
                    borrow_maxTime.value = "23:59";
                    return_minTime.value = '00:00';
                }
            }
        };

        const scrollToMap = () => {
            const mapElement = document.querySelector('.map');
            if (mapElement) {
                mapElement.scrollIntoView({ behavior: 'smooth' });
            }
        };

        const handleTypeChange = () => {
            if (formData.value.search_type == "1") {
                borrow_minDate.value = new Date().toISOString().split('T')[0];
                borrow_minTime.value = new Date().toLocaleTimeString('it-IT').slice(0, 5);
                return_minDate.value = new Date().toISOString().split('T')[0];
                return_minTime.value = new Date().toLocaleTimeString('it-IT').slice(0, 5);
                borrow_maxDate.value = return_minDate.value;
                borrow_maxTime.value = return_minTime.value;
                formData.value.borrow_date = new Date().toISOString().split('T')[0];
                formData.value.borrow_time = new Date().toLocaleTimeString('it-IT').slice(0, 5);
                formData.value.return_date = new Date().toISOString().split('T')[0];
                formData.value.return_time = new Date().toLocaleTimeString('it-IT').slice(0, 5);
            } else if (formData.value.search_type == "2") {
                borrow_minDate.value = new Date().toISOString().split('T')[0];
                borrow_minTime.value = new Date().toLocaleTimeString('it-IT').slice(0, 5);
                return_minDate.value = "2200-12-31"
                return_minTime.value = "23:59"
                borrow_maxDate.value = "2200-12-31"
                borrow_maxTime.value = "23:59"
                formData.value.borrow_date = new Date().toISOString().split('T')[0];
                formData.value.borrow_time = new Date().toLocaleTimeString('it-IT').slice(0, 5);
                formData.value.return_date = new Date().toISOString().split('T')[0];
                formData.value.return_time = new Date().toLocaleTimeString('it-IT').slice(0, 5);
            } else if (formData.value.search_type == "3") {
                borrow_minDate.value = new Date().toISOString().split('T')[0];
                borrow_minTime.value = new Date().toLocaleTimeString('it-IT').slice(0, 5);
                return_minDate.value = new Date().toISOString().split('T')[0];
                return_minTime.value = new Date().toLocaleTimeString('it-IT').slice(0, 5);
                borrow_maxDate.value = "2200-12-31"
                borrow_maxTime.value = "23:59"
                formData.value.borrow_date = new Date().toISOString().split('T')[0];
                formData.value.borrow_time = new Date().toLocaleTimeString('it-IT').slice(0, 5);
                formData.value.return_date = new Date().toISOString().split('T')[0];
                formData.value.return_time = new Date().toLocaleTimeString('it-IT').slice(0, 5);
            }
        }

        const saveQueryToHistory = (queryData, recommendedLocation) => {
            const history = JSON.parse(localStorage.getItem('queryHistory')) || [];
            const date = new Date().toISOString().split('T')[0];
            const time = new Date().toLocaleTimeString('it-IT').slice(0, 5);
            if(queryData.search_type == "1")
                history.push({ ...queryData, recommendedLocation,date,time});
            else if (queryData.search_type == "2")
            {
                queryData.return_date = "無";
                queryData.return_time = "";
                history.push({ ...queryData, recommendedLocation,date,time});
            }
            else if (queryData.search_type == "3")
            {
                queryData.borrow_date = "無";
                queryData.borrow_time = "";
                history.push({ ...queryData, recommendedLocation,date,time});
            }
            localStorage.setItem('queryHistory', JSON.stringify(history));
            loadQueryHistory();
        };

        const loadQueryHistory = () => {
            const history = JSON.parse(localStorage.getItem('queryHistory')) || [];
            queryHistory.value = history;
        };

        const removeExpiredQueries = () => {
            const now = new Date();
            const validQueries = queryHistory.value.filter(query => {
                let DateTime
                if(query.search_type == "1")
                    DateTime = new Date(`${query.return_date}T${query.return_time}`);
                else if (query.search_type == "2")
                    DateTime = new Date(`${query.borrow_date}T${query.borrow_time}`);
                else if (query.search_type == "3")
                    DateTime = new Date(`${query.return_date}T${query.return_time}`);
                    return DateTime > now;
            });
            localStorage.setItem('queryHistory', JSON.stringify(validQueries));
            queryHistory.value = validQueries;
        };


        return {
            formData,
            return_minDate,
            return_minTime,
            borrow_minDate,
            borrow_minTime,
            borrow_maxDate,
            borrow_maxTime,
            handleSubmit,
            borrowLocation,
            returnLocation,
            borrowRecommendedLocation,
            returnRecommendedLocation,
            updateBorrowLocation,
            updateReturnLocation,
            handleBorrowDateChange,
            handleReturnDateChange,
            handleTypeChange,
            queryHistory, // 用於存儲查詢紀錄
            itemsPerPage,
            currentPage,
            totalPages,
            paginatedHistory,
            nextPage,
            prevPage,
            goToPage
        };
    }
};
</script>

<style scoped>
body {
    font-family: 'Roboto', sans-serif;
    background: linear-gradient(to right, #2c3e50, #4ca1af);
    color: #333;
}

.map {
    height: 70vh;
    width: 80vw;
    margin: 20px auto;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    border-radius: 10px;
    background-color: #ffffff;
    /* 更明亮的背景顏色 */
}

.form-container {
    width: 80vw;
    max-width: 600px;
    padding: 20px;
    margin-top: 20px;
    background: rgba(255, 255, 255, 0.9);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    margin-bottom: 20px;
    color: #333;
}

.form-container .form-group {
    width: 100%;
    margin-bottom: 15px;
}

.form-container .form-label {
    font-weight: bold;
    margin-bottom: 5px;
    display: block;
}

.form-container .form-control, .form-container .form-select {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
}

.form-container .btn {
    align-self: center;
    padding: 10px 20px;
    background-color: #3498db;
    color: #fff;
    border: none;
    border-radius: 5px;
    transition: background-color 0.3s ease;
}

.form-container .btn:hover {
    background-color: #2980b9;
}

.query-history {
    background: rgba(0, 0, 0, 0.8);
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    padding: 20px;
}

.query-history h3 {
    color: #fff;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.card {
    border: none;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.card-header {
    background: #3498db;
    color: #fff;
    font-weight: bold;
    text-align: center;
    padding: 10px;
}

.card-body {
    background: #fff;
    color: #333;
    padding: 15px;
    text-align: left;
}

.pagination-container {
    display: flex;
    justify-content: center;
}

.page-item.disabled .page-link, .page-item.active .page-link {
    background-color: #3498db;
    color: #fff;
    border-color: #3498db;
}

.page-link {
    color: #3498db;
    transition: background-color 0.3s ease;
}

.page-link:hover {
    background-color: #2980b9;
    color: #fff;
}

.color-0 { background-color: #ffadad; }
.color-1 { background-color: #ffd6a5; }
.color-2 { background-color: #fdffb6; }
.color-3 { background-color: #caffbf; }
.color-4 { background-color: #9bf6ff; }
</style>
