<template>
    <header>
        <div class="container">
            <h1>YouBike 2.0 Recommendation System</h1>
            <p>Explore and find the best bike rental stations near you!</p>
            <!-- Description of four status types -->
            <div class="status-types">
                <div class="status">
                    <img src="normal.ico" alt="Normal"> Normal Availability
                </div>
                <div class="status">
                    <img src="no_bike.ico" alt="No Bikes"> No Bikes Available
                </div>
                <div class="status">
                    <img src="full.ico" alt="Full"> Station Full
                </div>
                <div class="status">
                    <img src="closed.ico" alt="Closed"> Station Closed
                </div>
            </div>
        </div>
    </header>
</template>

<script>
export default {
    name: 'HeaderSection'
}
</script>

<style scoped>
header {
    background-color: #007bff;
    /* Example background color */
    color: #fff;
    /* Example text color */
    padding: 20px;
}

.status-types {
    display: flex;
    justify-content: space-around;
    margin-top: 10px;
}

.status {
    text-align: center;
}

.status img {
    width: 40px;
    height: 40px;
    margin-bottom: 5px;
}
</style>