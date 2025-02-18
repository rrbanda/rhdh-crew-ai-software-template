# Use Red Hat UBI9 as the base image
FROM registry.access.redhat.com/ubi9/python-311:latest

# Set environment variables
ENV APP_HOME=/app
WORKDIR $APP_HOME

# Ensure root permissions during installation
USER root

# Install build dependencies for SQLite compilation
RUN dnf install -y gcc make tar wget gzip && \
    dnf clean all

# Manually install SQLite 3.41+
RUN wget https://www.sqlite.org/2023/sqlite-autoconf-3410000.tar.gz && \
    tar -xvzf sqlite-autoconf-3410000.tar.gz && \
    cd sqlite-autoconf-3410000 && \
    ./configure --prefix=/usr/local && \
    make -j$(nproc) && make install && \
    cd .. && rm -rf sqlite-autoconf-3410000 sqlite-autoconf-3410000.tar.gz && \
    ldconfig && \
    sqlite3 --version  # Verify installation

# Ensure Python uses the correct SQLite version
ENV LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"
ENV PATH="/usr/local/bin:$PATH"
RUN python3 -c "import sqlite3; print('SQLite version:', sqlite3.sqlite_version)"  # Debugging check

# ✅ Ensure group and user exist before adding, **but don't force UID 1001**
RUN groupadd -r appgroup || true && \
    useradd -r -g appgroup appuser || true

# Create necessary directories and fix permissions
RUN mkdir -p /opt/app-root/src/.local/share/app && \
    chown -R appuser:appgroup /opt/app-root/src/.local

# Copy application files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Set correct permissions for non-root user
RUN chown -R appuser:appgroup $APP_HOME && chmod -R 775 $APP_HOME

# Switch to non-root user
USER appuser

# Expose port for FastAPI
EXPOSE 8000

# Set default command
CMD ["python", "-m", "src.main", "--mode", "api"]
