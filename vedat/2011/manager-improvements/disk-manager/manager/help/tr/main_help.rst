Disk Yöneticisi
---------------

**Disk Yöneticisi** ile  sisteminizde bulunan disk bölümlerinin sistem açılışında nasıl başlatılacağının ayarlarını yapabilirsiniz. Diskler bu ayar ile, sistemin dosya sistemi içerisindeki yerlerini alırlar. Böylece her açışılışta sisteme disklerinizi yeniden elle bağlamak zorunda kalmazsınız. Disk Yöneticisi ile ayrıca o an sistemde bulunan diskleri sisteme bağlayıp sistemden ayırabilirsiniz.


Otomatik Bağlama İçin Kayıt Ekleme
----------------------------------

Bilgisayarı her açtığınızda bir disk bölümünün, dosya sisteminin belirli bir noktasına bağlanmasını istiyorsanız **Disk Yöneticisi** ile bir kayıt eklemelisiniz. Kayıt eklemek için **Disk Yöneticisinin** listelediği disklerden bağlamak istediğinizi seçiniz. Listenin altındaki alandan 'Otomatik Bağla' adlı seçim kutusunu işaretleyip bağlama işlemi ile ilgili değerleri ayarlayın. Bu değerler şunlardır:

* Bağlama Noktası: Disk bölümünün sistemin dosya sistemi içerisinde yerleşeceği noktadır. Genelde '/media' ya da '/mount' dizinleri altında bir dizin tercih edilir (Örneğin /media/Bellek).
* Dosya Sistemi Tipi: Disk bölümünüzün dosya sistemi tipi. Disk bölümünü oluştururken belirlemiş olduğunuz tipi seçin. Eğer disk bölümünüzün dosya sistemi tipinin ne olduğunu bilmiyorsanız kabuktan 'blkid' komutunun çıktısını inceleyip öğrenebilirsiniz.
* Ek Seçenekler: Disk bölümünün açılışta sisteme bağlanması anında sistemin bağlama işlemi için kullanacağı seçenekler buraya yazılır. **Disk Yöneticisi** seçtiğiniz dosya sistemi tipi için ön tanımlı seçenekleri sizin için buraya ekliyor. İsterseniz buraya başka seçenekler de ekleyebilirsiniz. Seçeneklerin neler olabileceği ile ilgili detaylı bilgiye 'mount' komutunun man sayfasından erişebilirsiniz. Seçenekleri yazdığınız yerin yanındaki 'Sıfırla' adlı buton ile ön tanımlı değerlere dönebilirsiniz.

Bu adımlardan sonra 'Kaydet' butonu ile kaydı ekleyebilirsiniz. Ekleme sırasında bir sorun olursa sistem sizi bilgilendirecektir. Sorun olmadığı takdirde kayıt eklendikten sonra eğer disk bölümü sisteme bağlı değilse sisteme bağlanacaktır.


Kayıt Silme
-----------

Eklediğiniz bir kaydı silmek için ilgili disk bölümünü seçip listenin altındaki 'Otomatik Bağla' seçim kutusundaki işareti kaldırın ve 'Kaydet' butonuna tıklayın.


Bölüm Bağlama
-------------

Bir disk bölümünü sisteme bağlamak için listeden seçip 'Bağla' butonuna tıklayın.


Bölüm Ayırma
------------

Bir disk bölümünü sistemden ayırmak için listeden seçip 'Ayır' butonuna tıklayın.


