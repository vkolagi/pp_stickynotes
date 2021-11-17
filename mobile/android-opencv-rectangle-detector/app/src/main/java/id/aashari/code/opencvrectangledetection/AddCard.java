package id.aashari.code.opencvrectangledetection;

import android.content.Context;
import android.content.ContextWrapper;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;
import android.os.Environment;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Base64;
import android.util.Log;
import android.util.Property;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import org.json.JSONObject;
import org.opencv.core.Mat;
import org.opencv.imgproc.Imgproc;

import java.io.ByteArrayOutputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.UnknownHostException;


import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;
import okhttp3.MultipartBody;
import okhttp3.MultipartBody.Builder;
import org.opencv.imgcodecs.Imgcodecs;




public class AddCard extends AppCompatActivity {
    protected String m_resultText = "aa";
    public static String uploadImage(File file) {

        try {

            final MediaType MEDIA_TYPE_PNG = MediaType.parse("image/jpeg");

            RequestBody req = new MultipartBody.Builder().
                    setType(MultipartBody.FORM)
                    .addFormDataPart("file","image_rotated.jpg",
                            RequestBody.create(MEDIA_TYPE_PNG, file)).build();

            Request request = new Request.Builder()
                    .url("http://192.168.1.240:8000/image-to-text")
                    .post(req)
                    .build();

            OkHttpClient client = new OkHttpClient();
            Response response = client.newCall(request).execute();


            String jsonData = response.body().string();
            //Log.d("response", "uploadImage:"+ response.body().string());
            JSONObject Jobject = new JSONObject(jsonData);
            return Jobject.getString("extracted_text");
            //return new JSONObject(response.body().string());

        } catch (UnknownHostException | UnsupportedEncodingException e) {
            Log.e("Error", "Error: " + e.getLocalizedMessage());
        } catch (Exception e) {
            Log.e("Error", "Other Error: " + e.getLocalizedMessage());
        }
        return "";
    }

    private String saveToInternalStorage(Bitmap bitmapImage){
        ContextWrapper cw = new ContextWrapper(getApplicationContext());
        // path to /data/data/yourapp/app_data/imageDir
        File directory = new File(Environment.getExternalStorageDirectory() + "/Images/");
        // Create imageDir
        File mypath=new File(directory,"image_rotated.jpg");

        FileOutputStream fos = null;
        try {
            fos = new FileOutputStream(mypath);
            // Use the compress method on the BitMap object to write image to the OutputStream
            bitmapImage.compress(Bitmap.CompressFormat.PNG, 100, fos);
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                fos.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return directory.getAbsolutePath();
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_card2);
        final File path = new File(Environment.getExternalStorageDirectory() + "/Images/");
        final File imgFile = new File(path, "image.jpg");
        TextView resultText = (TextView) findViewById(R.id.resultText);
        
        if(imgFile.exists()){
            Bitmap myBitmap = BitmapFactory.decodeFile(imgFile.getAbsolutePath());
            Matrix matrix = new Matrix();
            matrix.postRotate(90);
            Bitmap rotatedBitmap = Bitmap.createBitmap(myBitmap, 0, 0,
                    myBitmap.getWidth(), myBitmap.getHeight(), matrix, true);
            ImageView myImage = (ImageView) findViewById(R.id.imageViewPers);
            myImage.setImageBitmap(rotatedBitmap);
            saveToInternalStorage(rotatedBitmap);


            new Thread(new Runnable() {
                private volatile String m_result= "";
                public String getResult() {
                    return m_result;
                }
                @Override
                public void run() {
                    final File imgFileRot = new File(path, "image_rotated.jpg");
                    m_result  = uploadImage(imgFileRot);
                    TextView resultText = (TextView) findViewById(R.id.resultText);
                    /*try{
                        resultText.setText(response);
                    }
                    catch (Throwable tx) {
                        Log.e("err", "unexpected result");
                    }*/
                }
            }).start();


        }
    }
}