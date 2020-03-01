var page = 1;
function OnSubmitFilters(user_id = -1) {
    if (user_id == -1) {
        action_string= `/observations/list/all?page=${page}`;
    } else if (user_id > 0) {
        action_string = `/observations/list/${user_id}?page=${page}`
    } else {
        action_string = `/observations/listuser?page=${page}`;
    }
    document.filterForm.action = action_string; 
};
function onPageButtonClick(page_num) {
    page = page_num;
};