from django.urls import path
from .utils.base import *
from .utils.login import *
from .utils.registrationsApi import *
from .utils.remote import *
from django.conf.urls.static import static
from .views import *
from .utils.dataupload import *
from .utils.fetchdetails import *
from .utils.CreateUserDetails import *
from .utils.AddCard import *
from .utils.ClusterProducts import *
from .utils.buynow import *
from .utils.reviews import *
from .utils.forgate_password import *
from .utils.orderhistory import *
from .utils.visitservicecenter import *
from .testings import *
from . import *
# live
urlpatterns = [
    path('',base_index,name='base_index'),
    path('login',login_panel,name='login_panel'),
    path('registration',registration,name='registration'),
    path('create_registration',create_registration,name='create_registration'),
    path('create-login',create_login_api,name='create-login'),
    path('check_user_login',check_user_login,name='check_user_login'),
    path('products-category',accessories_remote,name='products-category'),
    path('products_details',products_details,name='products_details'),
    path('file_upload',file_upload,name='file_upload'),
    path('upload_csv',upload_csv,name='upload_csv'),
    path('fetch_details',fetch_details,name='fetch_details'),
    path('fetch_item_details/<int:item_id>/', fetch_item_details, name='fetch_item_details'),
    path('bose-products/<path:item_slug>/', fetch_item_detailsss, name='bose-products'),
    path('createuser', UserDetailsView, name='createuser'),
    path('BuyProductsView',BuyProductsView.as_view(),name='BuyProductsView'),
    path('add_to_card',add_to_cart,name='add_to_card'),
    path('shopping-Cart',viewAddDetails,name='shopping-Cart'),
    path('countaddcard',countaddcard,name='countaddcard'),
    path('update_add_card_details',UpdateAddcardDetails,name='update_add_card_details'),
    path('type_colors/<int:item_id>/',item_colors_view,name='type_colors'),
    path('color_types',color_types,name='color_types'),
    path('filterations_color',filterations_color,name='filterations_color'),
    path('chekout_now',chekout_now,name='chekout_now'),
    path('customer-details',userscreations_data,name='customer-details'),
    path('abouts-us',abouts_us,name='abouts-us'),
    path('our-services',service_panel,name='our-services'),
    path('contact-us',contacte_us,name='contact-us'),
    path('ClusteringDetails',ClusteringDetails,name='ClusteringDetails'),
    path('buy_products/<path:item_slug>/',buy_products,name='buy_products'),
    path('BuyNowView',BuyNowView.as_view(),name='BuyNowView'),
    path('add-to-wishlist/', add_to_wishlist, name='add_to_wishlist'),
    path('get-wishlist-count/', get_wishlist_count, name='get_wishlist_count'),
    path('wishlist',wishlist, name='wishlist'),
    path('update_wish_list_details',update_wish_list_details, name='update_wish_list_details'),
    path('countwishcard',countwishcard,name='countwishcard'),
    path('shipping-policy',shipping_policy,name='shipping-policy'),
    path('privacy-policy',privacy_policy,name='privacy-policy'),
    path('refund-returns-policy',refund_returns_policy,name='refund-returns-policy'),
    path('cancellation-policy',cancellation_policy,name='cancellation-policy'),
    path('add-review/', add_review, name='add-review'),
    path("fetch_reviews",fetch_reviews, name="fetch_reviews"),      
    path('like_unlike_review/',like_unlike_review, name='like_unlike_review'),
    path('profile',profile_base,name='profile'),
    path('get_profile',get_profile,name='get_profile'),
    path('update_profile',update_profile,name='update_profile'),
    path('delete_account', userAccountDelete, name='delete_account'),
    path('check_login',check_login,name='check_login'),
    path('logout', logout_user, name='logout'),
    path('change-password',change_password,name='change-password'),
    path('forgate-password',forgate_password,name='forgate-password'),
    path('send_otp',send_otp,name='send_otp'),
    path('verify_otp',verify_otp,name='verify_otp'),
    path('reset_password',reset_password,name='reset_password'),
    # path('payments-return-response',payment_returns,name='payments-return-response'), # for product based url
    path('order_confirmation_response',payment_returns,name='order_confirmation_response'), # for product based url
    path("payment-returns-buynow",payment_returns_buynow,name='payment-returns-buynow'),
    path('pdfgenerateHtml',pdfgenerateHtml,name='pdfgenerateHtml'),
    path('check_user_logged_in',check_user_logged_in,name='check_user_logged_in'),
    path("check_username",check_username,name='check_username'),
    path("check_email",check_email,name='check_email'),
    path('change_profile_data',change_profile,name='change_profile_data'),
    path('get_user_profile',get_user_profile,name='get_user_profile'),
    path('order-history',orderHistory_customer,name='order-history'),
    path('update-status', update_payment_status, name='update-status'),
    path("share_products",share_products,name='share_products'),
    path("appointment_form",appointment_form,name='appointment_form'),
    # offsite visit
    path("offsite_visit",offsite_visit,name='offsite_visit'),
    path("onside-visit-appointments",onside_visit_appointments.as_view(),name='onside-visit-appointments'),
    path("payment-return-response",payment_online,name='payment-return-response'),  # for appointment based url
    path('count_likes_dislikes',count_likes_dislikes,name='count_likes_dislikes'),
    path('onsite_slot_check_book',onsite_slot_check_book,name='onsite_slot_check_book'),
    path('offsite_slot_check_book',offsite_slot_check_book,name='offsite_slot_check_book'),
    path("robots", robots_txt,name='robots'),
    path('send_whatsapp_message', send_whatsapp_messagess, name='send_whatsapp_message'),
    path('whatsapp_page', whatsapp_page, name='whatsapp_page'),
    path('services/bose-service-center', testings_data, name='bose-service-center'),
    path('services/bose-service-center-mumbai', bose_service_center_mumbai, name='bose-service-center-mumbai'),
    path('services/bose-speaker-service-center',bose_speaker_service,name='bose-speaker-service-center'),
    path('services/bose-service-center-andheri',bose_service_center_andheri,name='bose-service-center-andheri'),
    path('services/bose-service-center-thane',bose_service_center_thane,name='bose-service-center-thane'),
    path('services/bose-service-center-in-india',bose_service_center_india,name='bose-service-center-in-india'),
    path('services/bose-service-center-andheri-east',bose_service_center_andheri_east,name='bose-service-center-andheri-east'),
    path('services/bose-service-center-nagpur',bose_service_center_nagpur,name='bose-service-center-nagpur'),
    path('services/bose-service-center-andheri-west',boseservice_center_andheri_west,name='bose-service-center-andheri-west'),
    path('services/bose-service-center-in-thane',bose_service_center_in_thane,name='bose-service-center-in-thane'),
    path('services/bose-headphone-cushion-replacement',bose_headphone_cushion_replacement,name='bose-headphone-cushion-replacement'),
    path('services/bose-speaker-repair',bose_speaker_repair,name='bose-speaker-repair'),
    path('services/repair-bose-speakers-mumbai',repair_bose_speakers_mumbai,name='repair-bose-speakers-mumbai'),
    path('collection/bose-portable-bluetooth-speaker',bose_portable_bluetooth_speaker,name='bose-portable-bluetooth-speaker'),
    path('collection/bose-soundbar',bose_soundbar,name='bose-soundbar'),
    path('collection/bose-headphone-cushions',bose_headphone_cushions,name='bose-headphone-cushions'),
    path('api/scrape-reviews', scrape_google_reviews, name='scrape-reviews'),
    path('collection/small-bluetooth-speaker',small_bluetooth_speaker,name='small-bluetooth-speaker'),
    path('collection/best-soundbar-under-20000',best_soundbar_under,name='best-soundbar-under-20000'),
    path('collection/bose-remote-control',bose_remote_control,name='bose-remote-control'),


    # =====================blogs section ============================================================
    path('blogs/how-to-repair-bose-bluetooth-speaker',blogs_bose_bluetooth_speaker,name='how-to-repair-bose-bluetooth-speaker'),  # how to repair bose bluetooth speaker
    path('blogs/best-bluetooth-speaker',best_bluetooth_speaker_blogs,name='best-bluetooth-speaker'),  # Best bluetooth speaker
    path('blogs/how-to-connect-bluetooth-speaker-to-pc',Best_bluetooth_speaker_pc_blogs,name='how-to-connect-bluetooth-speaker-to-pc'),  # how to connect bluetooth speaker to pc
    path('blogs/how-to-connect-bluetooth-speaker-to-laptop',connect_bluetooth_speaker_laptop_blogs,name='how-to-connect-bluetooth-speaker-to-laptop'),  # how to connect bluetooth speaker to laptop
    path('blogs/bluetooth-headphone',bluetooth_headphone_blogs,name='bluetooth-headphone'),  # bluetooth headphone
    path('blogs/which-bluetooth-headphone-is-best',bluetooth_headphone_best_blogs,name='which-bluetooth-headphone-is-best'),  # which bluetooth headphone is best
    path('blogs/best-bluetooth-speaker-sound-quality',best_bluetooth_speaker_sound_blogs,name='best-bluetooth-speaker-sound-quality'),  # best bluetooth speaker sound quality
    path('blogs/how-to-use-alexa-as-bluetooth-speaker',alexa_bluetooth_speaker_blogs,name='how-to-use-alexa-as-bluetooth-speaker'),  # how to use alexa as bluetooth speaker
    path('blogs/best-bluetooth-speaker-for-home',best_bluetooth_speaker_home_blogs,name='best-bluetooth-speaker-for-home'),  # best bluetooth speaker for home
    path('blogs/best-soundbar-in-india',best_soundbar_in_india_blogs,name='best-soundbar-in-india'),  # best soundbar in india
    path('blogs/how-to-connect-soundbar-to-tv',connect_soundbar_tv_blogs,name='how-to-connect-soundbar-to-tv'),  # how to connect soundbar to tv
    path('blogs/bose-speakers-price',bose_speakers_price_blogs,name='bose-speakers-price'),  # bose speakers price
    path('blogs/which-headphone-is-best',which_headphone_is_bests,name='which-headphone-is-best'),  # which headphone is best
    path('blogs/what-is-headphone',what_is_headphones,name='what-is-headphone'),  # what is headphone
    path('blogs/how-to-connect-headphone-with-mobile',connect_headphone_with_mobile,name='how-to-connect-headphone-with-mobile'),  # how to connect headphone with mobile
    path('blogs/how-to-clean-headphone-cushions',clean_headphone_cushions,name='how-to-clean-headphone-cushions'),  # how to clean headphone cushions
    path('blogs/how-to-repair-headphone',how_to_repair_headphones,name='how-to-repair-headphone'),  # how to repair headphone
    path('blogs/which-headphone-is-good-for-ear',which_headphone_is_good_ears,name='which-headphone-is-good-for-ear'),  # which headphone is good for ear
    path('blogs/how-to-connect-bluetooth-speaker',how_to_connect_bluetooth_speakers,name='how-to-connect-bluetooth-speaker'),  # how to connect bluetooth speaker
    path('blogs/which-soundbar-is-best',which_soundbar_is_bests,name='which-soundbar-is-best'),  # which soundbar is best
    path('blogs/what-is-soundbar',what_is_soundbars,name='what-is-soundbar'),  # what is soundbar
    path('blogs/bose-service-center-in-worli', bose_service_center_in_worlis, name='bose-service-center-in-worli'),
    path('blogs/bose-service-center-in-mulund', bose_service_center_in_mulunds, name = 'bose-service-center-in-mulund'),
    path('blogs/bose-service-center-in-juhu', bose_service_center_in_juhus, name = 'bose-service-center-in-juhu'),
    path('blogs/bose-service-center-in-prabhadevi', bose_service_center_in_prabhadevis, name = 'bose-service-center-in-prabhadevi'),
    path('blogs/bose-service-center-in-bhandup', bose_service_center_in_bhandups, name = 'bose-service-center-in-bhandup'),
    path('blogs/bose-service-center-in-bandra', bose_service_center_in_bandras, name = 'bose-service-center-in-bandra'),
    path('blogs/bose-service-center-in-matunga', bose_service_center_in_matungas, name = 'bose-service-center-in-matunga'),
    path('blogs/bose-service-center-in-nahur', bose_service_center_in_nahurs, name = 'bose-service-center-in-nahur'),
    path('blogs/bose-service-center-in-santacruz', bose_service_center_in_santacruzs, name = 'bose-service-center-in-santacruz'),
    path('blogs/bose-service-center-in-mahim', bose_service_center_in_mahims, name = 'bose-service-center-in-mahim'),
    path('blogs/bose-service-center-in-kanjurmarg', bose_service_center_in_kanjurmargs, name = 'bose-service-center-in-kanjurmarg'),
    path('blogs/bose-service-center-in-khar', bose_service_center_in_khars, name = 'bose-service-center-in-khar'),
    path('blogs/bose-service-center-in-lower-parel', bose_service_center_in_lower_parels, name = 'bose-service-center-in-lower-parel'),
    path('blogs/bose-service-center-in-vikhroli', bose_service_center_in_vikhrolis, name = 'bose-service-center-in-vikhroli'),
    path('blogs/bose-service-center-in-versova', bose_service_center_in_versovas, name = 'bose-service-center-in-versova'),
    path('blogs/bose-service-center-in-sion', bose_service_center_in_sions, name = 'bose-service-center-in-sion'),
    path('blogs/bose-service-center-in-ghatkopar', bose_service_center_in_ghatkopars, name = 'bose-service-center-in-ghatkopar'),
    path('blogs/bose-service-center-in-lokhandwala', bose_service_center_in_lokhandwalas, name = 'bose-service-center-in-lokhandwala'),
    path('blogs/bose-service-center-in-wadala', bose_service_center_in_wadalas, name = 'bose-service-center-in-wadala'),
    path('blogs/bose-service-center-in-powai', bose_service_center_in_powais, name = 'bose-service-center-in-powai'),
    path('blogs/bose-service-center-in-goregaon', bose_service_center_in_goregaons, name = 'bose-service-center-in-goregaon'),
    path('blogs/bose-service-center-in-parel', bose_service_center_in_parels, name = 'bose-service-center-in-parel'),
    path('blogs/bose-service-center-in-chembur', bose_service_center_in_chemburs, name = 'bose-service-center-in-chembur'),
    path('blogs/bose-service-center-in-malad', bose_service_center_in_malads, name = 'bose-service-center-in-malad'),
    path('blogs/bose-service-center-in-byculla', bose_service_center_in_bycullas, name = 'bose-service-center-in-byculla'),
    path('blogs/bose-service-center-in-kurla', bose_service_center_in_kurlas, name = 'bose-service-center-in-kurla'),
    path('blogs/bose-service-center-in-kandivali', bose_service_center_in_kandivalis, name = 'bose-service-center-in-kandivali'),
    path('blogs/bose-service-center-in-marine-lines', bose_service_center_in_marine_liness, name = 'bose-service-center-in-marine-lines'),
    path('blogs/bose-service-center-in-vashi', bose_service_center_in_vashis, name = 'bose-service-center-in-vashi'),
    path('blogs/bose-service-center-in-jogeshwari', bose_service_center_in_jogeshwaris, name = 'bose-service-center-in-jogeshwari'),
    path('blogs/bose-service-center-in-grant-road', bose_service_center_in_grant_roads, name = 'bose-service-center-in-grant-road'),
    path('blogs/bose-service-center-in-airoli', bose_service_center_in_airolis, name = 'bose-service-center-in-airoli'),
    path('blogs/bose-service-center-in-dahisar', bose_service_center_in_dahisars, name = 'bose-service-center-in-dahisar'),
    path('blogs/bose-service-center-in-mumbai-central', bose_service_center_in_mumbai_centrals, name = 'bose-service-center-in-mumbai-central'),
    path('blogs/bose-service-center-in-kalyan-dombivli', bose_service_center_in_kalyan_dombivlis, name='bose-service-center-in-kalyan-dombivli'),
    path('blogs/bose-service-center-in-borivali', bose_service_center_in_borivalis, name='bose-service-center-in-borivali'),
    path('blogs/bose-service-center-in-cst', bose_service_center_in_csts, name='bose-service-center-in-cst'), 





        


    path('blogs/which-soundbar-is-best-for-home',which_soundbar_is_best_homes,name='which-soundbar-is-best-for-home'),  # which soundbar is best for home
    path('manual-appointment/', create_manual_appointment, name='create_manual_appointment'),
    path('manual-slot-check/', manual_slot_check_book, name='manual_slot_check_book'),
    path('cashfree/webhook',cashfree_webhook, name='cashfree_webhook'),
    path("test-404/", test_404),
    path('blogs/bose-service-center-in-dombivli', bose_service_center_in_dombivlis, name='bose-service-center-in-dombivli'),
    path('blogs/bose-service-center-in-marol', bose_service_center_in_marols, name='bose-service-center-in-marol'),
    path('blogs/bose-service-center-in-fort', bose_service_center_in_forts, name='bose-service-center-in-fort'),
    path('blogs/bose-service-center-in-ambernath', bose_service_center_in_ambernaths, name='bose-service-center-in-ambernath'),
    path('blogs/bose-service-center-in-saki-naka', bose_service_center_in_saki_nakas, name='bose-service-center-in-saki-naka'),
    path('blogs/bose-service-center-in-colaba', bose_service_center_in_colabas, name='bose-service-center-in-colaba'),
    path('blogs/bose-service-center-in-kalwa', bose_service_center_in_kalwas, name='bose-service-center-in-kalwa'),
    path('blogs/bose-service-center-in-chakala', bose_service_center_in_chakalas, name='bose-service-center-in-chakala'),
    path('blogs/bose-service-center-in-charni-road', bose_service_center_in_charni_roads, name='bose-service-center-in-charni-road'),
    path('blogs/bose-service-center-in-mumbra', bose_service_center_in_mumbras, name='bose-service-center-in-mumbra'),
    path('blogs/bose-service-center-in-dn-nagar', bose_service_center_in_dn_nagars, name='bose-service-center-in-dn-nagar'),
    path('blogs/bose-service-center-in-elphinstone', bose_service_center_in_elphinstones, name='bose-service-center-in-elphinstone'),
    path('blogs/bose-service-center-in-titwala', bose_service_center_in_titwalas, name='bose-service-center-in-titwala'),
    path('blogs/bose-service-center-in-oshiwara', bose_service_center_in_oshiwaras, name='bose-service-center-in-oshiwara'),
    path('blogs/bose-service-center-in-tardeo', bose_service_center_in_tardeos, name='bose-service-center-in-tardeo'),
    path('blogs/bose-service-center-in-badlapur', bose_service_center_in_badlapurs, name='bose-service-center-in-badlapur'),
   path('blogs/bose-service-center-in-vile-parle', bose_service_center_in_vile_parles, name='bose-service-center-in-vile-parle'),
   path('blogs/bose-service-center-in-chinchpokli', bose_service_center_in_chinchpoklis, name='bose-service-center-in-chinchpokli'),
   path('blogs/bose-service-center-in-sanpada', bose_service_center_in_sanpadas, name='bose-service-center-in-sanpada'),
   path('blogs/bose-service-center-in-turbhe', bose_service_center_in_turbhes, name='bose-service-center-in-turbhe'),
  path('blogs/bose-service-center-in-ghansoli', bose_service_center_in_ghansolis, name='bose-service-center-in-ghansoli'),
  path('blogs/bose-service-center-in-andheri', bose_service_center_in_andheris, name='bose-service-center-in-andheri'),
  path('blogs/bose-service-center-in-thane', bose_service_center_in_thanes, name='bose-service-center-in-thane'),
path('blogs/bose-service-center-in-dadar', bose_service_center_in_dadars, name='bose-service-center-in-dadar'),








]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
