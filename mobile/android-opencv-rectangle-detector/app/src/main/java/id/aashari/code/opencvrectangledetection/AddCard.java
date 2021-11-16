package id.aashari.code.opencvrectangledetection;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;
import android.os.Environment;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Base64;
import android.util.Property;
import android.view.View;
import android.widget.ImageView;

import org.opencv.core.Mat;
import org.opencv.imgproc.Imgproc;

import java.io.ByteArrayOutputStream;
import java.io.File;



public class AddCard extends AppCompatActivity {



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_card2);
        File path = new File(Environment.getExternalStorageDirectory() + "/Images/");
        File imgFile = new File(path, "image.png");
        if(imgFile.exists()){
            Bitmap myBitmap = BitmapFactory.decodeFile(imgFile.getAbsolutePath());
            Matrix matrix = new Matrix();
            matrix.postRotate(90);
            Bitmap rotatedBitmap = Bitmap.createBitmap(myBitmap, 0, 0,
                    myBitmap.getWidth(), myBitmap.getHeight(), matrix, true);
            ImageView myImage = (ImageView) findViewById(R.id.imageViewPers);
            myImage.setImageBitmap(rotatedBitmap);
        }
    }
}