// toaster
function toaster(heading='Oop`s', message='I didn`t understand, Please inform to admin.', type='info')
{
    types = ['primary', 'danger', 'success', 'warning', 'info'];
    if(jQuery.inArray(type, types) == -1)
    {
        type = 'info';
    }
    var toast = '<div class="toast bg-'+type+'" role="alert" aria-live="assertive" aria-atomic="true" data-autohide="false"><div class="toast-header bg-'+type+'"><strong class="mr-auto text-white">'+heading+'</strong><button type="button" onclick="removeToast(this);" class="ml-2 mb-1 close" data-dismiss="toast">&times;</button></div><div class="toast-body">'+message+'</div></div>';
    $('#toast_stack').prepend(toast);
    $('.toast').toast('show');
}

function removeToast(button)
{
    $(button).parent().parent().remove();
}