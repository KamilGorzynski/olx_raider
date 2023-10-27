FROM public.ecr.aws/lambda/python:3.11 as build
RUN yum install -y unzip && \
    curl -Lo "/tmp/chromedriver-linux64.zip" "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/118.0.5993.70/linux64/chromedriver-linux64.zip" && \
    curl -Lo "/tmp/chrome-linux64.zip" "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/118.0.5993.70/linux64/chrome-linux64.zip" && \
    unzip /tmp/chromedriver-linux64.zip -d /opt/ && \
    unzip /tmp/chrome-linux64.zip -d /opt/

FROM public.ecr.aws/lambda/python@sha256:a8770bd841c9caa98557ef7dc590bbd2707eb5ecab13bc8edbc81bf4961dca61
RUN yum install atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel -y \

RUN pip install selenium==4.14.0

COPY --from=build /opt/chrome-linux64 /opt/chrome

COPY --from=build /opt/chromedriver-linux64 /opt/

COPY lambda_function.py ${LAMBDA_TASK_ROOT}

COPY lambda_utils ${LAMBDA_TASK_ROOT}/lambda_utils

COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt


CMD ["lambda_function.lambda_handler"]