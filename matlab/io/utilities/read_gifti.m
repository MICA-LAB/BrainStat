function gii = read_gifti2(file)

% Check for correct file.
if ~endsWith(file,'.gii')
    error('This function only accepts GIFTI files.');
end
if endsWith(file,'.func.gii')
    error('This function is unable to open .func.gii files.');
end

% Convert GIFTI file to a structure.
xml = xml2struct(file);
if ~iscell(xml.GIFTI.DataArray)
    xml.GIFTI.DataArray = {xml.GIFTI.DataArray};
end

% Decode data.
path = string(fileparts(file));
for ii = 1:numel(xml.GIFTI.DataArray)
    data = decode_array(xml.GIFTI.DataArray{ii}, path);    
    
    switch xml.GIFTI.DataArray{ii}.Attributes.Intent
        case 'NIFTI_INTENT_LABEL'
            gii.cdata = data;
            for jj = 1:numel(xml.GIFTI.LabelTable.Label)
                gii.labels.name{jj} = xml.GIFTI.LabelTable.Label{jj}.CDATA;
                gii.labels.rgba(jj,:) = [str2double(xml.GIFTI.LabelTable.Label{jj}.Attributes.Red), ...
                    str2double(xml.GIFTI.LabelTable.Label{jj}.Attributes.Green), ...
                    str2double(xml.GIFTI.LabelTable.Label{jj}.Attributes.Blue), ...
                    str2double(xml.GIFTI.LabelTable.Label{jj}.Attributes.Alpha)];
                gii.labels.key(jj) = str2double(xml.GIFTI.LabelTable.Label{jj}.Attributes.Key);
            end
        case {'NIFTI_INTENT_SHAPE','NIFTI_INTENT_NORMAL'}
            gii.cdata = data; 
        case 'NIFTI_INTENT_TRIANGLE'
            gii.faces = data+1;
        case 'NIFTI_INTENT_POINTSET'
            gii.vertices = data;
            gii.mat = str2num(xml.GIFTI.DataArray{1}.CoordinateSystemTransformMatrix.MatrixData.Text);
        otherwise
            error('Unknown GIFTI intent.')
    end              
end
end

%% Support functions
function output_data = decode_array(array,path)

% Get array properties
encoding = array.Attributes.Encoding;
coded_data = array.Data.Text;
datatype = array.Attributes.DataType;
datatype = regexp(datatype,'_[A-Z]+[0-9]+','match','once');
datatype = lower(datatype(2:end));
switch datatype
    case 'float32'
        datatype = 'single';
    case 'float64'
        datatype = 'double';
end

for ii = 1:str2double(array.Attributes.Dimensionality)
    dim(ii) = str2double(array.Attributes.(['Dim' num2str(ii-1)]));
end

% Decode data array
[~,~,machine_encoding] = fopen(1); 
if (array.Attributes.Endian == "LittleEndian" && contains(machine_encoding,'ieee-be')) || (array.Attributes.Endian == "BigEndian" && ~contains(machine_encoding,'ieee-le'))
    swap = @swapbytes;
else
    swap = @(x) x; 
end

switch encoding
    case {'ASCII','ExternalFileBinary'}
        if encoding == "ASCII"
            decoded_data = str2num(coded_data);  %#ok<ST2NM>
        elseif encoding == "ExternalFileBinary"
            fid = fopen(path + filesep + array.Attributes.ExternalFileName);
            if fid == -1
                error('Unable to find the external binary file.');
            end
            fseek(fid,str2double(array.Attributes.ExternalFileOffset),0);
            decoded_data = fread(fid,prod(dim),datatype);
        end
        fun = str2func(datatype);
        decoded_data = fun(decoded_data);
        if encoding == "ExternalFileBinary"
            decoded_data = swap(decoded_data);
        end
    case {'Base64Binary','GZipBase64Binary'}
        import matlab.net.base64decode
        decoded = base64decode(coded_data);
        if encoding == "GZipBase64Binary"
            decoded = chunkDunzip(decoded);
        end
        decoded_data = typecast(swap(decoded),datatype);
    otherwise
        error('Unknown encoding.')
end

% Reshape array
if array.Attributes.Dimensionality == "1"
    output_data = decoded_data(:);
elseif array.Attributes.Dimensionality == "2"
    output_data = reshape(decoded_data, str2double(array.Attributes.Dim1), ...
        str2double(array.Attributes.Dim0))';
else
    error('Unknown dimensionality.');
end
end

function U = chunkDunzip(Z)
% Praise stackoverflow
% (https://stackoverflow.com/questions/46733632/gzip-in-matlab-for-big-files)
% Modified from stackoverflow to output to a variable rather than a file. 

% Imports:
import com.mathworks.mlwidgets.io.InterruptibleStreamCopier

% Definitions:
MAX_CHUNK = 100*1024*1024; % 100 MB, just an example

% Split to chunks:
nChunks = ceil(numel(Z)/MAX_CHUNK);
chunkBounds = round(linspace(0, numel(Z), max(2,nChunks)) );

V = java.util.Vector();
for indC = 1:numel(chunkBounds)-1
  V.add(java.io.ByteArrayInputStream(Z(chunkBounds(indC)+1:chunkBounds(indC+1))));
end

S = java.io.SequenceInputStream(V.elements);  
b = java.util.zip.InflaterInputStream(S);

isc = InterruptibleStreamCopier.getInterruptibleStreamCopier;
c = java.io.ByteArrayOutputStream;
isc.copyStream(b,c);
U = c.toByteArray;
end