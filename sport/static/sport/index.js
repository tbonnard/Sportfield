document.addEventListener("DOMContentLoaded", function () {
    document.querySelector('#parent_list_field').style.display='none';
    document.querySelector('#form_booking').style.display='none';
    document.querySelector('#thank_you').style.display='none';
    document.querySelector('#error_sorry').style.display='none';


     

                document.querySelectorAll('#category_button').forEach(category_button => {
                        category_button.onclick = function () {
                                // scroll up to see the top of the page
                                window.scrollTo({ top: 0});
                                const category = this.dataset.category;

                                document.querySelector('#parent_list_field').style.display='block';
                                document.querySelector('#list_cat').style.display='none';
                                document.querySelector('#section_top').style.display='none';
                                document.querySelector('#list_field').style.display='none';
                                
                                // determine the current date
                                var date = new Date();
                                var today = date.getFullYear().toString() + '-' + (date.getMonth() + 1).toString().padStart(2, 0) +
                                '-' + date.getDate().toString().padStart(2, 0);
                                var time = date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds();
                                //console.log(today);
                                //console.log(time);
                                document.querySelector('#date_input').min = today;
                                
                                
                                // Fetch data of the available fields based on the category selected by the user and the date
                                document.querySelectorAll('#date_input').forEach(date_input => {
                                    date_input.onchange = function () {

                                        document.querySelector('#no_field').style.display='none'; 
                                        document.querySelectorAll(".row").forEach(e => e.parentNode.removeChild(e));
                                        let date_selected =  document.querySelector('#date_input').value;
                                        //console.log(date_selected);

                                        fetch(`/get_fields/${category}/${date_selected}`)
                                        .then(response => response.json())
                                            .then(fields => {

                                                    if (fields.length > 0) { 
                                                        fields.forEach(field => {
                                                            //console.log(field);

                                                                    document.querySelector('#list_field').style.display='block';    
                                                                     
                                                                    // for each field, the elements are created
                                                                    const row = document.createElement('div');
                                                                    row.className='row';
                                                                    row.style.marginTop = '20px';
                                                                    row.style.backgroundColor='rgb(245, 245, 245)';
                                                                    
                                                                    const h5 = document.createElement('h5');
                                                                    h5.className='card-body';
                                                                    h5.innerHTML = `${field.field_name}`;
                                                                    row.appendChild(h5);
            
                                                                    const p0 = document.createElement('p');
                                                                    p0.className='card-text';
                                                                    p0.innerHTML = `$${field.price} per hour`;
                                                                    row.appendChild(p0);
            
                                                                    // const p = document.createElement('p');
                                                                    // p.className='card-text';
                                                                    // p.innerHTML = `${field.address} ${field.address_number} ${field.city} ${field.zip_code} ${field.country}`;
                                                                    // row.appendChild(p);
                                                                
                                                                    const iframe = document.createElement('iframe');
                                                                    iframe.src =`http://maps.google.com/maps?q=${field.full_address}&z=14&output=embed`;
                                                                    iframe.style.height = '200px';
                                                                    iframe.style.width = '100%';
                                                                    row.appendChild(iframe);

                                                                    const select_button = document.createElement('button');
                                                                    select_button.textContent = 'Book';
                                                                    select_button.dataset.field = `${field.id}`;
                                                                    select_button.dataset.date = `${date_selected}`;
                                                                    select_button.id = 'select_button_field';
                                                                    select_button.className = 'btn btn-success'
                                                                    row.appendChild(select_button);
            
                                                                    document.querySelector('#list_field').append(row);
                                                                        
                                                                                            
                                                                        // when a user selects an available field, bookin view is called to book based on the date/field
                                                                        document.querySelectorAll('#select_button_field').forEach(select_button_field_button => {
                                                                            select_button_field_button.onclick = function () {
            
                                                                                    let field = this.dataset.field;
                                                                                    let date = this.dataset.date;
                                                                                    console.log(field)
                                                                                    console.log(date)

                                                                                    document.querySelector('#parent_list_field').style.display='none';
                                                                                    document.querySelector('#form_booking').style.display='block';
                                                                                    document.querySelector('#do_you_confirm').disabled = true;



                                                                                    //GET SCHEDULES FIELD
                                                                                    fetch(`/schedule/${field}/${date}`)
                                                                                    .then(response => response.json())
                                                                                        .then(schedules => {
                                                                                            
                                                                                                                                                      
                                                                                            let select_time_field = document.querySelector('#select_time_field')

                                                                                            const select_time_input = document.createElement('select');
                                                                                            select_time_input.id = 'select_a_time_for_booking';
                                                                                            select_time_field.appendChild(select_time_input);

                                                                                            const default_option_time = document.createElement('option')
                                                                                            default_option_time.value = "select_a_time";
                                                                                            default_option_time.innerHTML = "select a time";
                                                                                            select_time_input.appendChild(default_option_time);

                                                                                            schedules.forEach(schedule => {
                                                                                                console.log(schedule)
                                                                                                
                                                                                                let option_time = document.createElement('option')
                                                                                                option_time.value = `${schedule.schedule_time}`;
                                                                                                option_time.innerHTML = `${schedule.schedule_time}`;                                                                                    
                                                                                                select_time_input.appendChild(option_time);

                                                                                                document.querySelectorAll('#select_a_time_for_booking').forEach(time_selected_option => {
                                                                                                    
                                                                                                    time_selected_option.onchange = function () {
                                                                                                        
                                                                                                        let time = this.value
                                                                                                        console.log(date + ' ' + field + ' ' + time)

                                                                                                        if (time !='select_a_time') {
                                                                                                            document.querySelector('#do_you_confirm').disabled = false;

                                                                                                            document.querySelector('#do_you_confirm').onclick = function () {
                                                                                                               
                                                                                                                // no need to that as data is sent with param directly
                                                                                                                const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                                                                                                                const request = new Request(
                                                                                                                    '/booking',
                                                                                                                    {headers: {'X-CSRFToken': csrftoken}}
                                                                                                                );
                                                                                                                fetch(request, {
                                                                                                                    method: 'POST',
                                                                                                                    mode: 'same-origin',
                                                                                                                    body: JSON.stringify({
                                                                                                                        field: field,
                                                                                                                        date: date,
                                                                                                                        time: time,
                                                                                                                        })
                                                                                                                    })
                                                                                                                    .then(response => response.json())
                                                                                                                    .then(result => {
                                                                                                                        console.log(result)
                                                                                                                        if (result.message === 'OK') 
                                                                                                                            {document.querySelector('#thank_you').style.display='block';
                                                                                                                            document.querySelector('#form_booking').style.display='none';                                                                                                                       
                                                                                                                            }
                                                                                                                        else {
                                                                                                                            document.querySelector('#form_booking').style.display='none';                                                                                                                       
                                                                                                                            document.querySelector('#error_sorry').style.display='block';
                                                                                                                        }

                                                                                                                 

                                                                                                                    });
                                                                                                                    return false;

                                                                                                            }

                                                                                                        } else {
                                                                                                            document.querySelector('#do_you_confirm').disabled = true;
                                                                                                        }
                                                                                                    
                                                                                                    }
                                
                                                                                                })

                                                                                    
                                                                                            });


                                                                                        });

                                                                                   

                                                                                      

                                                                            }
                                                                        });

                                                        });
                                        
                                                    } else {
                                                            //console.log('no field');
                                                            document.querySelector('#no_field').style.display='block';      
                                                            document.querySelector('#no_field').innerHTML = "There's is no available field sorry. Select another date or sport.";
                                                    }
                                            });

                                }
                            });
                        }
                });

        // hide / unhide elements based on user interactions : when he cancels the search
    document.querySelector('#button_cancel_field_list').onclick = function () {
        document.querySelector('#parent_list_field').style.display='none';
        document.querySelector('#list_cat').style.display='block';
        document.querySelector('#section_top').style.display='block';
        document.querySelector('#no_field').style.display='none';
        document.querySelectorAll(".row").forEach(e => e.parentNode.removeChild(e));


    }

});