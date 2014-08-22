package DrM_Peak;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import jxl.Cell;
import jxl.Sheet;
import jxl.Workbook;
import jxl.read.biff.BiffException;

public class ReadExcel {
	
	
	public List<Double> readread (File file, int colnum) throws BiffException, IOException {
		ReadExcel readexcel = new ReadExcel(); 
		return readexcel.excelRead(new File("Workbook1.xls"), colnum );
	}

	public List<Double> excelRead(File file, int colnum) throws BiffException, IOException {
		List<Double> data = new ArrayList<Double>();
		double num;
		String tempstring; 
		
		Workbook w = Workbook.getWorkbook(file);
		Sheet sheet = w.getSheet(0);
		
		//for (int col = 0; col < sheet.getColumns(); col++){
		
		for (int row = 0; row < sheet.getRows(); row++) {
			Cell cell = sheet.getCell(colnum, row);
			tempstring = cell.getContents();
			num = Double.parseDouble(tempstring);
			data.add(num);
		}
		
		
		return data;
	}
	
	
	
}
